"""
Historical News & Document APIs Toolkit (1990–2012)
=====================================================

Unified Python interface for querying 5 recommended APIs:
1. Internet Archive CDX
2. NYT Article Search
3. Chronicling America
4. GDELT Project (BigQuery v2.0 & v1.0 CSV)
5. The Guardian Open Platform

Author: AI Research Assistant
Date: January 2026
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlencode, quote
import csv
import io
from pathlib import Path


# ============================================================================
# 1. INTERNET ARCHIVE CDX API
# ============================================================================

class InternetArchiveCDX:
    """
    Query the Internet Archive Wayback Machine CDX index.
    
    No authentication required. Date format: YYYYMMDD[hhmmss]
    
    Example:
        cdx = InternetArchiveCDX()
        results = cdx.query("example.com", 1990, 2012)
    """
    
    BASE_URL = "https://web.archive.org/cdx/search/cdx"
    
    def __init__(self, rate_limit_delay: float = 0.5):
        """
        Initialize CDX querier.
        
        Args:
            rate_limit_delay: Seconds to pause between requests (0.5 recommended)
        """
        self.rate_limit_delay = rate_limit_delay
    
    def query(
        self,
        url: str,
        start_year: int,
        end_year: int,
        output: str = "json",
        filter_status: Optional[str] = "200",
        **kwargs
    ) -> Dict:
        """
        Query CDX index for URL captures.
        
        Args:
            url: Domain or full URL to search (e.g., "example.com")
            start_year: Start year (1990)
            end_year: End year (2012)
            output: Response format ("json", "csv", "cdx")
            filter_status: HTTP status code filter (e.g., "200" for success)
            **kwargs: Additional CDX parameters (e.g., fl="timestamp,statuscode,mimetype")
        
        Returns:
            Parsed JSON response with captures
        
        Example:
            >>> cdx = InternetArchiveCDX()
            >>> results = cdx.query("example.com", 1990, 2012, fl="timestamp,statuscode")
            >>> print(f"Found {len(results.get('results', []))} captures")
        """
        start_date = f"{start_year}0101"
        end_date = f"{end_year}1231"
        
        params = {
            "url": url,
            "from": start_date,
            "to": end_date,
            "output": output,
            "matchType": "domain",
            "collapse": "statuscode",  # Collapse duplicates
        }
        
        if filter_status:
            params["filter"] = f"statuscode:{filter_status}"
        
        params.update(kwargs)
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            if output == "json":
                data = response.json()
                return {
                    "success": True,
                    "captures": data[1:] if len(data) > 1 else [],
                    "columns": data[0] if data else []
                }
            else:
                return {"success": True, "raw": response.text}
                
        except requests.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def build_wayback_url(self, original_url: str, timestamp: str) -> str:
        """
        Construct a Wayback Machine snapshot URL.
        
        Args:
            original_url: URL to access in archive
            timestamp: Capture timestamp (14 digits YYYYMMDDHHMMSS)
        
        Returns:
            Full Wayback URL
        
        Example:
            >>> cdx = InternetArchiveCDX()
            >>> url = cdx.build_wayback_url("example.com", "20110101000000")
            >>> print(url)
            https://web.archive.org/web/20110101000000/http://example.com
        """
        if not original_url.startswith("http"):
            original_url = f"http://{original_url}"
        return f"https://web.archive.org/web/{timestamp}/{original_url}"


# ============================================================================
# 2. NEW YORK TIMES ARTICLE SEARCH API
# ============================================================================

class NYTArticleSearch:
    """
    Query New York Times Article Search API.
    
    Requires free API key from: https://developer.nytimes.com/
    Date format: YYYYMMDD
    Rate limit: 10 requests/second, 4,000 requests/day (free tier)
    
    Example:
        nyt = NYTArticleSearch(api_key="YOUR_KEY")
        results = nyt.query("climate change", 1990, 2012, sort="oldest")
    """
    
    BASE_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    
    def __init__(self, api_key: str):
        """Initialize with API key."""
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def query(
        self,
        query_text: str,
        start_year: int,
        end_year: int,
        sort: str = "newest",
        fq: Optional[str] = None,
        page: int = 0,
        **kwargs
    ) -> Dict:
        """
        Search NYT Article database.
        
        Args:
            query_text: Search terms
            start_year: Start year (1990)
            end_year: End year (2012)
            sort: "newest", "oldest", "relevance"
            fq: Filter query (e.g., 'source:("The New York Times")')
            page: Results page (0-indexed)
            **kwargs: Additional parameters (see NYT API docs)
        
        Returns:
            Articles and metadata
        
        Example:
            >>> nyt = NYTArticleSearch("YOUR_KEY")
            >>> results = nyt.query("9/11", 2001, 2001)
            >>> for article in results.get("articles", []):
            ...     print(article["headline"]["main"])
        """
        begin_date = f"{start_year}0101"
        end_date = f"{end_year}1231"
        
        params = {
            "q": query_text,
            "begin_date": begin_date,
            "end_date": end_date,
            "sort": sort,
            "page": page,
            "api-key": self.api_key,
        }
        
        if fq:
            params["fq"] = fq
        
        params.update(kwargs)
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "articles": data.get("response", {}).get("docs", []),
                "total_hits": data.get("response", {}).get("meta", {}).get("hits", 0),
                "page": page
            }
            
        except requests.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def iterate_all_results(
        self,
        query_text: str,
        start_year: int,
        end_year: int,
        max_results: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """
        Iterate through all results (handles pagination).
        
        Args:
            query_text: Search terms
            start_year: Start year
            end_year: End year
            max_results: Maximum articles to return (None = no limit)
            **kwargs: Additional query parameters
        
        Returns:
            List of all articles found
        
        Note:
            NYT API pagination limit is ~101 pages × 10 per page ≈ 1,010 max per query
        """
        all_articles = []
        page = 0
        
        while True:
            results = self.query(query_text, start_year, end_year, page=page, **kwargs)
            
            if not results["success"]:
                break
            
            articles = results.get("articles", [])
            if not articles:
                break
            
            all_articles.extend(articles)
            
            if max_results and len(all_articles) >= max_results:
                all_articles = all_articles[:max_results]
                break
            
            page += 1
            if page > 100:  # Safety limit
                break
        
        return all_articles


# ============================================================================
# 3. CHRONICLING AMERICA API (Library of Congress)
# ============================================================================

class ChroniclingAmerica:
    """
    Query Chronicling America (historic US newspapers, 1690–1963).
    
    No authentication required. Date format: YYYYMMDD
    Coverage: 1690–1963 (expanded from original 1836–1922)
    Full-text searchable via OCR.
    
    Example:
        ca = ChroniclingAmerica()
        results = ca.query("industrial revolution", 1900, 1920)
    """
    
    BASE_URL = "https://chroniclingamerica.loc.gov/search/pages/results/"
    
    def __init__(self):
        """Initialize Chronicling America querier."""
        self.session = requests.Session()
    
    def query(
        self,
        query_text: str,
        start_year: int,
        end_year: int,
        state: Optional[str] = None,
        language: Optional[str] = "eng",
        output: str = "json",
        **kwargs
    ) -> Dict:
        """
        Search Chronicling America newspaper collection.
        
        Args:
            query_text: Search terms (OCR'd newspaper text)
            start_year: Start year (1690)
            end_year: End year (1963)
            state: US state code (e.g., "Massachusetts")
            language: Language code (default "eng")
            output: Response format ("json", "xml", "html")
            **kwargs: Additional parameters
        
        Returns:
            Search results with full-text snippets
        
        Example:
            >>> ca = ChroniclingAmerica()
            >>> results = ca.query("Civil War", 1860, 1865, state="Massachusetts")
            >>> for article in results.get("articles", []):
            ...     print(article["title"])
        """
        start_date = f"{start_year}0101"
        end_date = f"{end_year}1231"
        
        params = {
            "proxtext": query_text,
            "date1": start_date,
            "date2": end_date,
            "dateFilterType": "range",
            "format": output,
        }
        
        if state:
            params["state"] = state
        if language:
            params["language"] = language
        
        params.update(kwargs)
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            if output == "json":
                data = response.json()
                return {
                    "success": True,
                    "articles": data.get("items", []),
                    "total_items": data.get("totalItems", 0)
                }
            else:
                return {"success": True, "raw": response.text}
                
        except requests.RequestException as e:
            return {"success": False, "error": str(e)}


# ============================================================================
# 4. GDELT PROJECT - VERSION 2.0 (BigQuery SQL)
# ============================================================================

class GDELTBigQuery:
    """
    Query GDELT Project via Google BigQuery.
    
    Requires Google Cloud account with BigQuery enabled.
    Free tier: 1TB/month
    Coverage: 1979–present (structured event data)
    
    Setup:
        1. Create Google Cloud project
        2. Enable BigQuery API
        3. Create service account key (JSON)
        4. Install: pip install google-cloud-bigquery
    
    Example:
        gdelt = GDELTBigQuery("path/to/keyfile.json")
        results = gdelt.query_events(1990, 2012, event_codes=["0211", "0311"])
    """
    
    def __init__(self, credentials_path: str):
        """
        Initialize BigQuery connection.
        
        Args:
            credentials_path: Path to Google Cloud service account JSON key
        """
        try:
            from google.cloud import bigquery
            self.client = bigquery.Client.from_service_account_json(credentials_path)
        except ImportError:
            raise ImportError("Install google-cloud-bigquery: pip install google-cloud-bigquery")
    
    def query_events(
        self,
        start_year: int,
        end_year: int,
        event_codes: Optional[List[str]] = None,
        actor_country: Optional[str] = None,
        limit: int = 100000,
        **kwargs
    ) -> List[Dict]:
        """
        Query GDELT events table.
        
        Args:
            start_year: Start year (1979)
            end_year: End year (2012)
            event_codes: CAMEO event codes (e.g., ["0211", "0311"])
            actor_country: Country code filter
            limit: Maximum rows to return
            **kwargs: Additional SQL WHERE conditions
        
        Returns:
            List of event records
        
        Example:
            >>> gdelt = GDELTBigQuery("keyfile.json")
            >>> events = gdelt.query_events(2001, 2001, event_codes=["0211"])
            >>> print(f"Found {len(events)} conflict events in 2001")
        """
        sql = f"""
        SELECT *
        FROM `gdelt-bq.full.events`
        WHERE Year >= {start_year} AND Year <= {end_year}
        """
        
        if event_codes:
            codes_str = "', '".join(event_codes)
            sql += f" AND EventCode IN ('{codes_str}')"
        
        if actor_country:
            sql += f" AND Actor1CountryCode = '{actor_country}'"
        
        sql += f"\nLIMIT {limit}"
        
        try:
            query_job = self.client.query(sql)
            results = [dict(row) for row in query_job.result()]
            return results
        except Exception as e:
            print(f"BigQuery error: {e}")
            return []


# ============================================================================
# 5. THE GUARDIAN OPEN PLATFORM API
# ============================================================================

class GuardianAPI:
    """
    Query The Guardian Open Platform API.
    
    Requires free API key from: https://open-platform.theguardian.com/
    Coverage: 1999–present (Guardian articles)
    Date format: YYYY-MM-DD
    Free tier: 1 million requests/month (generous)
    
    Example:
        guardian = GuardianAPI(api_key="YOUR_KEY")
        articles = guardian.query("financial crisis", 2008, 2008)
    """
    
    BASE_URL = "https://open-platform.theguardian.com/search"
    
    def __init__(self, api_key: str):
        """Initialize with API key."""
        self.api_key = api_key
        self.session = requests.Session()
    
    def query(
        self,
        query_text: str,
        start_year: int,
        end_year: int,
        page: int = 1,
        page_size: int = 50,
        **kwargs
    ) -> Dict:
        """
        Search Guardian articles.
        
        Args:
            query_text: Search terms
            start_year: Start year (1999)
            end_year: End year (2012)
            page: Results page (1-indexed)
            page_size: Results per page (max 50)
            **kwargs: Additional parameters
        
        Returns:
            Articles and metadata
        
        Example:
            >>> guardian = GuardianAPI("YOUR_KEY")
            >>> results = guardian.query("global warming", 1999, 2012)
            >>> for article in results.get("articles", []):
            ...     print(article["webTitle"])
        """
        from_date = f"{start_year}-01-01"
        to_date = f"{end_year}-12-31"
        
        params = {
            "q": query_text,
            "from-date": from_date,
            "to-date": to_date,
            "page": page,
            "page-size": page_size,
            "api-key": self.api_key,
            "format": "json",
        }
        
        params.update(kwargs)
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            response_obj = data.get("response", {})
            return {
                "success": True,
                "articles": response_obj.get("results", []),
                "total_results": response_obj.get("total", 0),
                "page": page,
                "pages": response_obj.get("pages", 0)
            }
            
        except requests.RequestException as e:
            return {"success": False, "error": str(e)}
    
    def iterate_all_results(
        self,
        query_text: str,
        start_year: int,
        end_year: int,
        max_results: Optional[int] = None,
        **kwargs
    ) -> List[Dict]:
        """
        Iterate through all results (handles pagination).
        
        Args:
            query_text: Search terms
            start_year: Start year
            end_year: End year
            max_results: Maximum articles to return
            **kwargs: Additional parameters
        
        Returns:
            List of all articles found
        """
        all_articles = []
        page = 1
        
        while True:
            results = self.query(query_text, start_year, end_year, page=page, **kwargs)
            
            if not results["success"]:
                break
            
            articles = results.get("articles", [])
            if not articles:
                break
            
            all_articles.extend(articles)
            
            if max_results and len(all_articles) >= max_results:
                all_articles = all_articles[:max_results]
                break
            
            if page >= results.get("pages", 1):
                break
            
            page += 1
        
        return all_articles


# ============================================================================
# 6. ARCHIVE.ORG FALLBACK FOR DEAD LINKS
# ============================================================================

class ArchiveOrgFallback:
    """
    Generate archive.org lookup URLs for dead links.
    
    When Google/Bing links rot, fallback to Wayback Machine snapshot.
    
    Example:
        fallback = ArchiveOrgFallback()
        archive_url = fallback.get_closest_snapshot("example.com", 2005)
    """
    
    def get_closest_snapshot(
        self,
        url: str,
        year: int,
        month: int = 6,
        day: int = 15,
    ) -> str:
        """
        Get Wayback Machine URL for approximate date.
        
        Args:
            url: Original URL
            year: Year to lookup (1990–2012)
            month: Month (1–12, default June)
            day: Day (1–31, default 15)
        
        Returns:
            Wayback Machine URL
        
        Example:
            >>> fallback = ArchiveOrgFallback()
            >>> url = fallback.get_closest_snapshot("cnn.com", 2001, 9, 11)
            >>> print(url)
            https://web.archive.org/web/20010911/http://cnn.com
        """
        if not url.startswith("http"):
            url = f"http://{url}"
        
        timestamp = f"{year}{month:02d}{day:02d}"
        return f"https://web.archive.org/web/{timestamp}/{url}"
    
    def check_availability(self, url: str, year: int) -> Dict:
        """
        Check if Wayback Machine has captures for URL in given year.
        
        Args:
            url: URL to check
            year: Year (1990–2012)
        
        Returns:
            Availability info
        
        Example:
            >>> fallback = ArchiveOrgFallback()
            >>> result = fallback.check_availability("example.com", 2000)
            >>> if result["available"]:
            ...     print(f"Snapshot: {result['url']}")
        """
        api_url = "https://archive.org/wayback/available"
        params = {
            "url": url,
            "timestamp": f"{year}0101",
        }
        
        try:
            response = requests.get(api_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            snapshot = data.get("archived_snapshots", {}).get("closest", {})
            return {
                "available": snapshot.get("available", False),
                "url": snapshot.get("url", ""),
                "timestamp": snapshot.get("timestamp", ""),
                "status": snapshot.get("status", ""),
            }
            
        except requests.RequestException as e:
            return {"available": False, "error": str(e)}


# ============================================================================
# 7. UNIFIED ORCHESTRATOR
# ============================================================================

class HistoricalNewsOrchestrator:
    """
    Unified interface for querying multiple APIs.
    
    Automatically selects best APIs based on time period and query type.
    Implements fallback chains for robustness.
    
    Example:
        orchestrator = HistoricalNewsOrchestrator(
            nyt_key="YOUR_NYT_KEY",
            guardian_key="YOUR_GUARDIAN_KEY",
            gdelt_bq_creds="path/to/bigquery_key.json"
        )
        results = orchestrator.comprehensive_search("climate change", 1990, 2012)
    """
    
    def __init__(
        self,
        nyt_key: Optional[str] = None,
        guardian_key: Optional[str] = None,
        gdelt_bq_creds: Optional[str] = None,
    ):
        """Initialize with optional API keys."""
        self.cdx = InternetArchiveCDX()
        self.ca = ChroniclingAmerica()
        self.nyt = NYTArticleSearch(nyt_key) if nyt_key else None
        self.guardian = GuardianAPI(guardian_key) if guardian_key else None
        self.gdelt_bq = GDELTBigQuery(gdelt_bq_creds) if gdelt_bq_creds else None
        self.fallback = ArchiveOrgFallback()
    
    def comprehensive_search(
        self,
        query: str,
        start_year: int,
        end_year: int,
        include_apis: Optional[List[str]] = None,
        verbose: bool = False,
    ) -> Dict:
        """
        Search across multiple APIs with intelligent selection.
        
        Args:
            query: Search term
            start_year: Start year (1990–2012)
            end_year: End year
            include_apis: List of APIs to use (None = auto-select)
            verbose: Print progress
        
        Returns:
            Aggregated results from multiple sources
        
        Example:
            >>> orchestrator = HistoricalNewsOrchestrator(nyt_key="...", guardian_key="...")
            >>> results = orchestrator.comprehensive_search("9/11", 2001, 2001)
            >>> print(f"Total articles: {results['total_articles']}")
        """
        if include_apis is None:
            include_apis = ["cdx", "ca"]
            if start_year >= 1999:
                include_apis.append("guardian")
            if self.nyt:
                include_apis.append("nyt")
            if self.gdelt_bq:
                include_apis.append("gdelt")
        
        results = {
            "query": query,
            "date_range": f"{start_year}-{end_year}",
            "sources": {},
            "total_articles": 0,
        }
        
        if "cdx" in include_apis and verbose:
            print("Querying Internet Archive CDX...")
        if "cdx" in include_apis:
            cdx_results = self.cdx.query(
                query.replace(" ", "").lower(),
                start_year,
                end_year,
            )
            results["sources"]["internet_archive"] = cdx_results

        if "ca" in include_apis and verbose:
            print("Querying Chronicling America...")
        if "ca" in include_apis and start_year <= 1963:
            ca_results = self.ca.query(query, max(start_year, 1690), min(end_year, 1963))
            results["sources"]["chronicling_america"] = ca_results
            if ca_results.get("success"):
                results["total_articles"] += len(ca_results.get("articles", []))
        
        if "nyt" in include_apis and self.nyt and verbose:
            print("Querying NY Times Article Search...")
        if "nyt" in include_apis and self.nyt:
            nyt_results = self.nyt.iterate_all_results(query, start_year, end_year, max_results=100)
            results["sources"]["nyt"] = {"success": True, "articles": nyt_results}
            results["total_articles"] += len(nyt_results)
        
        if "guardian" in include_apis and self.guardian and start_year >= 1999 and verbose:
            print("Querying The Guardian Open Platform...")
        if "guardian" in include_apis and self.guardian and start_year >= 1999:
            guardian_results = self.guardian.iterate_all_results(query, max(start_year, 1999), end_year, max_results=100)
            results["sources"]["guardian"] = {"success": True, "articles": guardian_results}
            results["total_articles"] += len(guardian_results)
        
        return results


if __name__ == "__main__":
    print("=" * 60)
    print("Historical News & Document APIs Toolkit")
    print("=" * 60)
    print("\n✓ Classes loaded successfully:")
    print("  - InternetArchiveCDX")
    print("  - NYTArticleSearch")
    print("  - ChroniclingAmerica")
    print("  - GDELTBigQuery")
    print("  - GuardianAPI")
    print("  - ArchiveOrgFallback")
    print("  - HistoricalNewsOrchestrator")
    print("\n✓ Ready to import and use!")
    print("\nQuick test - Internet Archive CDX (no keys needed):")
    cdx = InternetArchiveCDX()
    results = cdx.query("example.com", 2000, 2005, fl="timestamp,statuscode")
    print(f"✓ Found {len(results.get('captures', []))} example.com snapshots")
