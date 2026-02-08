# Historical News & Document APIs Toolkit - README

**Complete Python toolkit for accessing 1990–2012 historical news and documents via official APIs, avoiding the "30-Day Trap"**

---

## 📋 Quick Start

### Installation

```bash
pip install requests google-cloud-bigquery
```

### Five-Minute Setup

```python
from historical_apis_toolkit import InternetArchiveCDX, ChroniclingAmerica

# No API keys needed for these:
cdx = InternetArchiveCDX()
results = cdx.query("example.com", 1990, 2012)
print(f"Found {len(results['captures'])} web captures")

ca = ChroniclingAmerica()
results = ca.query("World War II", 1939, 1945)
print(f"Found {results['total_items']} newspaper pages")
```

---

## 🔌 API Keys Required

### Internet Archive CDX
- **Cost:** Free | **Limit:** Unlimited | **Auth:** None

### New York Times Article Search
- **Cost:** Free | **Limit:** 10 req/sec, 4,000/day | **Auth:** API Key
- **Setup:** Visit https://developer.nytimes.com/

### Chronicling America
- **Cost:** Free | **Limit:** Unlimited | **Auth:** None

### GDELT BigQuery V2.0 (Recommended)
- **Cost:** Free | **Limit:** 1TB/month queries | **Auth:** Google Cloud
- **Setup:** Create Google Cloud project, enable BigQuery, create service account

### The Guardian Open Platform
- **Cost:** Free | **Limit:** 1 million requests/month | **Auth:** API Key
- **Setup:** Visit https://open-platform.theguardian.com/

---

## 🎯 Which API Should I Use?

### By Time Period

| Period | Primary API | Secondary |
|--------|-------------|-----------|
| 1690–1963 | Chronicling America | CDX |
| 1963–1999 | CDX | GDELT |
| 1999–2012 | CDX, NYT, GDELT | Guardian |

### By Query Type

| Query | Best API | Why |
|-------|----------|-----|
| Web snapshots | **CDX** | Complete web history |
| Historic newspapers | **Chronicling America** | ONLY full-text source for 1690–1963 |
| US news events | **NYT Article Search** | Highest quality |
| Global conflict/events | **GDELT BigQuery** | 35 years structured data |
| International news | **Guardian API** | Non-US perspective (1999+) |

---

## 💡 Common Use Cases

### Climate Change Coverage (1990–2012)

```python
from historical_apis_toolkit import HistoricalNewsOrchestrator

orchestrator = HistoricalNewsOrchestrator(
    nyt_key="YOUR_NYT_KEY",
    guardian_key="YOUR_GUARDIAN_KEY"
)

results = orchestrator.comprehensive_search(
    "climate change",
    1990,
    2012,
    verbose=True
)

print(f"Total articles found: {results['total_articles']}")
```

### 9/11 Coverage with Link Preservation

```python
from historical_apis_toolkit import NYTArticleSearch, ArchiveOrgFallback

nyt = NYTArticleSearch("YOUR_KEY")
articles = nyt.iterate_all_results("September 11", 2001, 2001, max_results=50)

fallback = ArchiveOrgFallback()
for article in articles[:5]:
    url = article.get("web_url", "")
    archive_url = fallback.get_closest_snapshot(url, 2001, 9, 11)
    print(f"Archive: {archive_url}")
```

### Global Conflict Events (GDELT)

```python
from historical_apis_toolkit import GDELTBigQuery

gdelt = GDELTBigQuery("/path/to/bigquery_key.json")

# CAMEO codes: 0211=Armed Attack, 0311=Military Material, 1011=Threat/Force
conflicts = gdelt.query_events(
    1990, 2012,
    event_codes=["0211", "0311", "1011"],
    actor_country="USA"
)

print(f"Found {len(conflicts)} conflict events")
```

### Historical Newspaper Search

```python
from historical_apis_toolkit import ChroniclingAmerica

ca = ChroniclingAmerica()

results = ca.query(
    "Industrial Revolution",
    1800, 1880,
    state="Massachusetts"
)

print(f"Found {results['total_items']} newspaper pages")
for page in results.get('articles', [])[:10]:
    print(f"  {page['title']} ({page.get('date_issued')})")
```

### Check Web Archive Coverage

```python
from historical_apis_toolkit import InternetArchiveCDX
from collections import defaultdict

cdx = InternetArchiveCDX()
results = cdx.query(
    "washingtonpost.com",
    1995, 2005,
    fl="timestamp,statuscode,mimetype"
)

# Timeline by year
by_year = defaultdict(int)
for capture in results['captures']:
    year = capture[0][:4]
    by_year[year] += 1

for year in sorted(by_year.keys()):
    print(f"  {year}: {by_year[year]} snapshots")
```

---

## ⚠️ "30-Day Trap" Explained

### What Is It?

Google/Bing re-index the web. If a page:
1. Hasn't been visited by crawlers in 30+ days
2. Original host has taken it down
3. Search engine hasn't re-crawled recently

**Result:** Page becomes invisible (even if archive.org has it)

### How This Toolkit Avoids It

| API | Strategy | Risk |
|-----|----------|------|
| **CDX** | Archives static snapshots | ✅ Zero |
| **NYT** | Indexes own archive (not live web) | ✅ Zero |
| **CA** | LoC-curated permanent collection | ✅ Zero |
| **GDELT** | Indexes published newsflow | ⚠️ Source links may rot |
| **Guardian** | Indexes Guardian archive | ✅ Zero |
| **Google/Bing** | Re-crawl live web | ❌ High |

---

## 📊 API Comparison Matrix

### Response Times
- **Instant:** CDX, Chronicling America, Guardian
- **1–5 sec:** NYT Article Search
- **5–30 sec:** GDELT BigQuery
- **Slow:** GDELT v1.0 CSV files (downloads)

### Rate Limits
- **Unlimited:** CDX, Chronicling America
- **10 req/sec:** NYT (4,000/day)
- **1M/month:** Guardian (very generous)
- **1TB/month:** GDELT BigQuery

### Full-Text Availability
- **Full-text:** Chronicling America (OCR'd newspapers)
- **Archive snapshots:** Internet Archive (original pages)
- **Snippets:** NYT, Guardian
- **Structured:** GDELT (metadata + event codes)

---

## 🔍 Date Formats by API

| API | Format | Example |
|-----|--------|---------|
| **CDX** | YYYYMMDD[hhmmss] | 19900101, 20010911120000 |
| **NYT** | YYYYMMDD | 19900101, 20121231 |
| **CA** | YYYYMMDD | 18361231, 19631231 |
| **GDELT** | YYYY (SQL) | Year >= 1990 AND Year <= 2012 |
| **Guardian** | YYYY-MM-DD | 1999-01-01, 2012-12-31 |

---

## 🛠️ Advanced Usage

### Batch Processing with CDX

```python
from historical_apis_toolkit import InternetArchiveCDX
import time

cdx = InternetArchiveCDX(rate_limit_delay=1.0)

urls = ["cnn.com", "bbc.com", "reuters.com"]
for url in urls:
    results = cdx.query(url, 1990, 2012, filter_status="200")
    print(f"{url}: {len(results['captures'])} captures")
    time.sleep(1.0)
```

### Fallback Chain for Dead Links

```python
from historical_apis_toolkit import ArchiveOrgFallback

fallback = ArchiveOrgFallback()

def get_article_safe(url, year):
    """Try live link, fallback to archive"""
    import requests
    try:
        return requests.get(url, timeout=5).text
    except:
        archive_url = fallback.get_closest_snapshot(url, year)
        return requests.get(archive_url, timeout=5).text
```

### Data Export to CSV

```python
from historical_apis_toolkit import NYTArticleSearch
import csv

nyt = NYTArticleSearch("YOUR_KEY")
articles = nyt.iterate_all_results("climate change", 1990, 2012)

with open("nyt_climate_1990_2012.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['pub_date', 'headline', 'url'])
    writer.writeheader()
    for article in articles:
        writer.writerow({
            'pub_date': article.get('pub_date'),
            'headline': article.get('headline', {}).get('main', ''),
            'url': article.get('web_url', ''),
        })

print(f"Exported {len(articles)} articles")
```

---

## 🐛 Troubleshooting

### "Connection timeout" errors
```python
cdx = InternetArchiveCDX(rate_limit_delay=2.0)
```

### "API key invalid" for NYT
```python
# Verify key at https://developer.nytimes.com/my-apps
# Ensure Article Search API is enabled
```

### BigQuery authentication fails
```bash
# Verify service account has "BigQuery User" role
gcloud iam service-accounts list
```

### "Too many requests" from CDX
```python
cdx = InternetArchiveCDX(rate_limit_delay=5.0)
```

---

## 📚 References

### Official Documentation
- [Internet Archive CDX API](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server)
- [NYT Article Search API](https://developer.nytimes.com/docs/articlesearch-product/1/overview)
- [Chronicling America API](https://chroniclingamerica.loc.gov/about/api/)
- [GDELT Project](https://www.gdeltproject.org/data.html)
- [Guardian Open Platform](https://open-platform.theguardian.com/)

---

## ✅ Checklist for Your First Query

- [ ] Install toolkit: `pip install requests`
- [ ] Identify your primary API
- [ ] Get API key (if required)
- [ ] Run example from this README
- [ ] Test with 1990–2012 date range
- [ ] Export results to CSV
- [ ] Archive important URLs to wayback.org

---

**Last Updated:** January 2026  
**Status:** Production-ready  
**Python:** 3.7+  
**License:** MIT

