# Internet Archive (Wayback Machine CDX API)

The Internet Archive's CDX API provides free access to historical web content (snapshots of webpages) dating back to the mid-1990s (e.g. earliest captures ~1996) – easily covering the 1990-2012 period. No API key is required ①. You query by URL or domain and can restrict by date using from and to parameters (inclusive) in timestamp format ②. The date syntax is flexible: you may use 1-14 digit dates (e.g. from=1990 for Jan 1 1990, or from=19900101000000 for a specific timestamp) ②. The API returns a list of archived captures (timestamp, original URL, etc.), which you can use to retrieve the page content. This is a full-text archive (HTML content of the pages), so you can obtain the entire page text. Link rot risk: Low – once a page is archived, the content is preserved. (If a page wasn't archived, it may be lost – so always verify archival.) The CDX API itself will list captures even if the original site is gone, enabling access via the Wayback Machine ③ ④.

Example: To find snapshots of example.com from 2005 to 2010, you could call:

<https://web.archive.org/cdx/search/cdx>?

url=example.com&amp;from=2005&amp;to=2010&amp;output=json

This returns capture data (e.g. timestamps). You can then construct a Wayback URL like https://

web.archive.org/web/<timestamp>/example.com to retrieve the archived page 4.

# New York Times Article Search API

The NYT Article Search API is free (with an API key) and provides article metadata and snippets dating back to 1851 ⑤ – well beyond 1990–2012. You can search by keywords, and filter by date range using

begin_date and end_date (YYYYMMDD format) ⑥. For example,

begin_date=19900101&amp;end_date=20121231 restricts results to that period. The free tier allows thousands of queries per day (rate-limited to ~10 requests/minute, 4000/day) and covers the entire archive. However, the API returns article metadata and short excerpts (e.g. headline, abstract, lead_paragraph) – not the full article text. You typically get a snippet or lead paragraph, and a URL to the NYT site ⑦. Full text is not provided due to copyright/paywall (articles 1923–1980 may require subscription on the NYT site). Link rot risk: Moderate – NYTimes keeps a stable archive, so article URLs remain valid, but content after 1980 might be behind a paywall (the API's snippet is the only freely accessible text) ⑤. For older public-domain articles (1851–1922) the full text is available via NYT archives, but the API still returns only metadata/snippets. In summary, NYT's API is excellent for historical search (even back to 1851) ⑤, but you'll likely need to visit or archive the article URL for the full text.

# The Guardian Open Platform (Content API)

The Guardian's Content API is free for non-commercial use and provides access to all Guardian content back to 1999 ⑧ (the archive covers when their digital content begins; content from the 1990s is available from 1999 onward). A free "developer" API key gives you up to 500 calls/day and includes full article text in the</timestamp>

response 9 10. You can search by keyword (q) and filter by date using from-date and to-date (format YYYY-MM-DD) 11. For example, from-date=2005-01-01&amp;to-date=2012-12-31 restricts results to 2005-2012. You can also filter by section, tags, etc., and request specific fields. To get article text, you add parameters like show-fields=body (or body-text) to include the full article content in results. The API returns JSON with fields such as title, publication date, and the body text (HTML or plain text). Link rot risk: Low - content comes directly from the Guardian's systems, so no dependency on external sites. Guardian articles are openly accessible and the API provides their text. In the free tier, you have all you need for textual analysis (no 30-day limit - it's the entire archive of ~1.9 million articles) 12. (For completeness: The Guardian's higher tiers mainly add images, multimedia, or higher call quotas 13, but for text content the free tier is sufficient.)

# Chronicling America (Library of Congress)

Coverage: Chronicling America is a collection of historic American newspapers, primarily from 1836-1963 14. (Content after 1963 is generally not included, so it does not cover 1990-2012. It's focused on older historical newspapers, often public domain material.) The data is free to access via the LOC API (no key required) 1. If your project extends to pre-1990 content, this API is invaluable; for 1990s-2000s content, it isn't applicable. You can search newspaper pages by keywords and date range. Date syntax: use start_date and end_date in YYYY-MM-DD format 15. For example:

<https://www.loc.gov/collections/chronicling-america/>? fo=json&amp;start_date=1910-01-01&amp;end_date=1910-12-31&amp;qs=influenza

This would search 1910 papers for "influenza". (qs is the query string parameter for keywords 16.) The results include metadata about newspaper pages that match, and often an OCR snippet of the text context. You can retrieve full OCR text of pages, but it may require an additional step (the API's search results might give a page ID and URL for the image/text; the actual text might be in an ocr field or a separate download). Content: The OCR text of scanned pages is available (since these are public-domain scans), though quality varies with scan quality. Link rot risk: Low - the Library of Congress hosts the content. Once digitized, those newspaper images and texts are stable on LOC servers. (The only "risk" is OCR errors, not link rot.) In summary, Chronicling America offers full text (via OCR) for very old newspapers (mostly pre-1964) for free 14, but it does not cover late-20th-century or early-21st-century news.

# GDELT Project (Version 1.0)

GDELT is an open dataset of global events. Version 1.0 covers January 1979 through early 2014 17 (specifically up to February 17, 2014, when GDELT 2.0 began). So it fully includes the 1990-2012 period. The data is  $100\%$  free and open 18. Coverage: GDELT isn't news articles per se, but a database of event records coded from news reports worldwide. Each record includes fields like date, location, actors, event type (CAMEO codes), tone, counts, etc., and often a source reference. It's updated daily (v1 was static after 2014; v2 is real-time) and spans the globe. You can access GDELT 1.0 in two main ways:

- BigQuery Public Dataset: Google BigQuery hosts GDELT; you can query the full 1979-present data in SQL 19. This is convenient for complex queries (filtering by event codes, actors, etc.) and large-scale analysis. BigQuery's free tier allows up to 1 TB of data processed per month, which covers quite

a lot of querying. For example, you could use BigQuery to filter events between 1990 and 2012 with specific keywords or codes in one SQL query. Pros: no need to download huge files, very fast queries. Cons: requires a Google Cloud account (free, but needs setup) and careful quota management. (No special API key beyond Google Cloud credentials; you can use the google-cloud-bigquery Python client or REST API. However, to keep things simple and free of heavy SDKs, you might choose the direct file route.)

- Direct CSV Files: GDELT provides raw data files (CSV, tab-separated) for all events. For GDELT 1.0, records are organized by date. Through March 2013, data is available as a backfile (e.g. yearly or one big ZIP)  $^{19}$ , and after April 1 2013, as daily update files  $^{19}$ . You can download these from GDELT's site (e.g. a master zip for 1979–2013, or year-by-year files  $^{20}$ ). The entire 1979–2013 dataset is large (on the order of a few gigabytes compressed, hundreds of millions of events), but you can download just the years of interest. Querying directly: You would download the CSV(s) and then use Python (pandas or even streaming line by line) to filter events by date, country, keywords, etc. This avoids any cloud usage limits (apart from your bandwidth/storage). For instance, to get events 1990–2012 about "United States", you could download each yearly file 1990.csv ... 2012.csv, then filter where Actor1CountryCode or Actor2CountryCode == USA, etc. This is feasible but can be heavy - using pandas to filter millions of rows will need memory. Still, for targeted queries it's workable. GDELT's own site suggests the entire database is ~quarter-billion records  $^{19}$ , so narrower filters (by date or event type) are fine.

Optimal method: If you have modest computing resources and want just a slice, downloading and parsing is free and avoids BigQuery's setup. If you need to aggregate or search through all events by complex criteria, BigQuery (with the free quota) is very powerful – just be mindful to limit data scanned (e.g. query specific date ranges or fields to stay under 1 TB/month). In practice, many researchers use BigQuery for GDELT  $^{21}$ $^{22}$  because of its ability to handle large scans quickly. But since the question emphasizes strictly free and no heavy SDKs, you might lean toward direct parsing with Python for specific queries.

Data content: GDELT does not provide full news article text – it provides structured data. Each event record has fields like actors, location, event code, tone, etc., and a citation (often a URL of a news article as SOURCEURL) that reported the event  $^{23}$ $^{24}$ . So you get the “who/what/where/when” of events, but not the narrative text from the article. The SOURCEURL field (introduced in late GDELT1.0) gives you a link to a news article or source for that event  $^{23}$ $^{24}$ . Link rot risk: Potentially high for those source URLs – they might be dead or moved after years. GDELT doesn’t host the articles, just the links. To mitigate this, you’d use the Wayback Machine fallback for those URLs. But GDELT itself is a stable, archived dataset. Once you have the events, the structured data is there permanently. In summary, GDELT (v1.0) is excellent for historical event data coverage (no 30-day limit at all – it’s decades of data) and is free, but remember you’ll only get metadata and coded fields, not the article text.

# Google Custom Search JSON API (Google Web Search)

If you need a general web search for historical content, Google's Custom Search JSON API allows querying Google's index programmatically. It's free for 100 queries/day (and can be increased with billing)  $^{25}$ $^{26}$ . You must create a Programmable Search Engine (which can be set to search the entire web) and use an API key  $^{27}$ $^{28}$ . This API returns web search results in JSON - including titles, snippet excerpts, URLs, etc., similar to what you see on Google's results page  $^{29}$ . You can incorporate Google's advanced search operators in the query string. In particular, Google supports the after: and before: operators to filter

by date (these accept YYYY-MM-DD or simpler dates). For example:

q="economic crisis" before:2012-01-01 after:2000-01-01

would ask for pages about "economic crisis" published between 2000 and 2011. In practice, Google's date operators work for far older dates – you can even do before:1990 (though you'll only get what's indexed, of course). Do they work reliably beyond 10 years? Generally yes – Google will attempt to filter by the page's date (often the indexed publication date). However, note that Google's dating of a page can be imperfect for very old pages. It might rely on detected dates on the page or crawl timestamps. Still, in testing, before: / after: does restrict results appropriately, and there's no hard cutoff at 10 years. Google's index includes content going back to the early web (and scanned books/newspapers in some cases). The main limitation is the 100/day query quota and that you only get snippets, not full text. Link rot risk: High if the page is no longer live – the API gives you the URL and snippet, but the page might 404 if it's very old. Google does not serve the page content. So you should use the returned URL with the Wayback Machine if needed. In summary, Google's API is great for finding which pages or articles exist for older queries, but you'll need to fetch or archive those pages to get the content. (No "30-day" limitation – Google will surface whatever is in its index, regardless of age, as long as your query is specific enough. For news, Google's index may not keep extremely old content if it disappeared from the web, which is why coupling with Wayback is wise.)

Note: Google shut down its old "Google News API"; the Custom Search API is the way to go for web/news queries now. It's free tier is fine for moderate use, and it does honor advanced operators. There is also a sort parameter (e.g. sort by date) and a dateRestrict in Programmable Search, but those are more limited. Using before:/after: in the query is the simplest way to enforce date ranges in the free API queries.

# Bing Web Search API

Bing's Web Search API (part of Azure Cognitive Services) can also retrieve web results via API. Free tiers typically allow around 1,000 queries/month (the exact quota can vary, e.g. 250/month on some plans, with option to pay for more). Bing's API supports keyword queries and returns JSON with results (title, snippet, URL, etc.). Regarding date filtering: Bing officially offers a freshness parameter, but it's primarily geared towards recent content. The documented options were "Day", "Week", or "Month" – which restrict to results from the last 24 hours, 7 days, or 30 days respectively. There isn't a straightforward public operator like Google's before: for arbitrary dates beyond the UI. In the Bing Web UI, you can set a custom date range, but the API's equivalent is not fully open. The Bing Web Search API (v7) does have an undocumented ability to specify a date range in the freshness parameter using a format like YYYY-MM-DD..YYYY-MM-DD, but it's limited. According to Microsoft's documentation, Bing's API date filter can only go up to 30 days in the past 30. In other words, Bing's API is not reliable for filtering results older than ~30 days on the free tier. If you try to use before:2010 in a Bing query, it likely won't work – Bing's search operators in general are not as flexible as Google's, and users have noted that before:/after: are not supported in Bing's query language (the Bing engine might ignore them) 31.

In practice, you can still search Bing for older content by keywords (it will return older pages if they are highly relevant), but you can't enforce a strict date cutoff beyond the built-in "past month" filter. So for

historical research, Bing is less useful via API. Link rot risk: Same as Google – Bing gives you the URL; if the site is dead or changed, you need an archive. Bing's index might retain snippet info for pages that have since vanished, but you'll only have the snippet. Also, Bing tends to be “more conservative” with older content 32 30 – notably, Bing will only return pages in date-filtered results if it has a clear datePublished metadata. Many older pages lack this, so they won't show up in date-restricted queries 33 . This means using Bing to discover deep historical content can miss a lot. Google's approach is a bit more lenient on what it considers “date”, so it often surfaces more old stuff with date operators. In summary, Bing's free API is fine for general web search, but for precise historical date ranges &gt;30 days, it's not reliable (the “30-day trap” hits here – Bing's free date filtering is essentially capped at 1 month) 30 .

# The "30-Day Trap" and Historical Access

Many news APIs impose a "last 30 days" limit on free access - meaning only recent news are available without paying. We've ensured the chosen APIs avoid this trap:

- Wayback Machine: No time limit - it's specifically for historical pages. You can retrieve pages decades old (if archived) for free.
- NYT Article API: No 30-day limit - it spans  $170+$  years. The free tier is intended for historical search (NYT encourages projects on their archive) 5.
- Guardian API: No recency limit - full archive since 1999 is open 8.
- Chronicling America: No recency limit (it's all historical by nature, up to 1963).
- GDELT: No limit - it's a historical dataset (1979-2014 for v1, with daily updates in v2).
- Google Custom Search: No built-in time restriction - you can search the whole web's history (to the extent content is indexed/available).
- Bing API: This is the one to watch - the free Bing News API only gives recent articles, and the Bing Web API's date filtering is effectively limited to  $\sim 30$  days past  $^{30}$ . So Bing is not great for targeted historical queries on the free tier. (It might still return old pages if you don't apply a date filter, but you can't reliably constrain to, say, the 1990s with the API.)

Full text vs Snippets: Out of our candidates, only some provide full article text on the free tier: The Wayback Machine provides the full page content (HTML) for archived pages; The Guardian API provides full article text 10 ; Chronicling America provides full OCR text of pages (since they're public domain). GDELT provides no article text - just metadata (and possibly an external URL). NYT API provides snippets/metadata, not full text. Google and Bing APIs provide only snippets (the search result excerpts) and URLs. So if full text is needed, you'll rely on those APIs that have it (Guardian, Chronicling, Wayback) or use the URLs from the others in combination with Wayback.

Below is a Historical API Matrix summarizing each provider:

|  Provider (API) | Max Historical Reach | Date Query Syntax | Content Returned | Link Rot Risk  |
| --- | --- | --- | --- | --- |
|  Internet Archive (Wayback CDX) | ~1996 - present (web pages) | from & to (timestamp or YYYY) 2 | Full page HTML (archived) | Low (archive copy is preserved)  |

|  Provider (API) | Max Historical Reach | Date Query Syntax | Content Returned | Link Rot Risk  |
| --- | --- | --- | --- | --- |
|  NYTimes Article Search | 1851 – present 5 | begin_date, end_date (YYYYMMDD) 6 | Metadata + snippet (no full text) | Moderate (NYT URLs stable, but paywalled content)  |
|  Guardian Content API | 1999 – present 8 | from-date, to-date (YYYY-MM-DD) 11 | Full article text (free tier) 10 | Low (content delivered via API)  |
|  Chronicling America | 1836 – 1963 14 | start_date, end_date (YYYY-MM-DD) 15 | OCR text of newspaper pages | Low (hosted by Library of Congress)  |
|  GDELT Project v1 | 1979 – Feb 2014 17 | filter by date in query or file (YYYYMMDD in data) | Structured events, no article text | High (URLs for sources may die; use archives)  |
|  Google Custom Search API | ~1990s – present (web index) | use before: / after: in query (YYYY-MM-DD) | Snippets + URLs (search results) | High (depends on external sites; many old links dead)  |
|  Bing Web Search API | ~1990s – present (web index) | Limited: freshness param (Day/Week/Month) – no full arbitrary date range 30 | Snippets + URLs (search results) | High (external sites; and date filter omits undated pages)  |

(Note: Bing's "custom date range" exists in web UI but not freely in API - essentially a 30-day cap on API date filters 30.)

As we can see, most of these are immune to the "30-day trap" – they allow historical queries well beyond 30 days. The only caution is Bing (and any strictly "news API" that wasn't listed in the query). By using sources like NYT, Guardian, archives, etc., we ensure free access to older material. For any links obtained (from NYT API, GDELT sources, Google/Bing results), we have a strategy to avoid link rot: use the Internet Archive as a fallback.

# Python Helper Functions for Historical Data APIs

Below are Python functions for the top five APIs/sources, each accepting start_year, end_year, and query (plus any needed API keys), and forming the appropriate API calls. These illustrate how to map our parameters to each API's syntax. We use simple requests.get calls for clarity, avoiding complex SDKs. (In production, you'd add error handling, rate-limit respect, pagination handling, etc., but we keep it minimal here.)

# 1. Wayback Machine CDX API - List archived URLs in date range

This function takes a target URL (or domain) and year range, and uses the CDX API to find archived

snapshots in that interval. It returns a list of captures (as JSON records). You could then retrieve content via the returned timestamps. We treat `query` as the URL to lookup in the archive (since Wayback doesn’t support keyword searches of content via API).

⬇
import requests

def list_wayback_snapshots(target_url, start_year, end_year):
"""
Query the Internet Archive CDX API for all snapshots of target_url
between start_year and end_year. Returns a list of snapshot records.
"""
base_url = "<http://web.archive.org/cdx/search/cdx>"
params = {
"url": target_url,
"from": str(start_year),
"to": str(end_year),
"output": "json"
}
response = requests.get(base_url, params=params)
response.raise_for_status()
return response.json() # list of [urlkey, timestamp, original, mime,
status, digest, length, ...]

Usage: `list_wayback_snapshots("http://example.com", 2000, 2005)` would list all archived snapshots of example.com from 2000 through 2005. (You can then pick a timestamp from the results and fetch the page via `requests.get("https://web.archive.org/web/<timestamp>/http://example.com")` to get the archived HTML.)

## 2 New York Times Article Search API – Search articles by keyword and date

This function searches NYT articles matching a query string in a given year range. It uses NYT’s `q` parameter for keywords and `begin_date` / `end_date` for date filtering. You need to provide your NYT API key. It returns the JSON response (which includes article metadata and snippets).

⬇
import requests

def search_nyt_articles(api_key, query, start_year, end_year):
"""
Search NYT articles containing the query between start_year and end_year.
Returns JSON response with article metadata.
"""
url = "<https://api.nytimes.com/svc/search/v2/articlesearch.json>"
params = {
"q": query,
"begin_date": f"{start_year}0101",
"end_date": f"{end_year}1231",

```txt
"api-key": api_key
}
response = requests.get(url, params=params)
response.raise_for_status()
return response.json()
```

Usage: search_nyt_articles(NYT_API_KEY, "Olympics", 1996, 2000) would retrieve articles mentioning "Olympics" from 1996-2000. The result's response['docs'] list contains articles with fields like headline, pub_date, snippet, etc. (Note: NYT API returns max 10 results per page; for extensive results you'd loop over page parameter. Here we just fetch the first batch for simplicity.)

## 3. The Guardian Content API – Search articles by keyword and date

This function uses the Guardian API to find articles matching a query in a date range. We include show-fields=body to retrieve the full text of articles. Provide your Guardian API key (developer key). It returns JSON data.

```python
import requests

def search_guardian(api_key, query, start_year, end_year):
''''
Search The Guardian for articles containing the query between start_year and end_year.
Returns JSON with articles (including full body text).
''''
url = "https://content.guardianapis.com/search"
params = {
"q": query,
"from-date": f"{start_year}-01-01",
"to-date": f"{end_year}-12-31",
"api-key": api_key,
"page-size": 50, # number of results per page (max 50 for Guardian API)
"show-fields": "body" # include full article text in the response
}
response = requests.get(url, params=params)
response.raise_for_status()
return response.json()
```

Usage: search_guardian(GUARDIAN_API_KEY, "climate change", 2005, 2010) would fetch up to 50 Guardian articles from 2005-2010 that mention "climate change," including their full text in the fields["body"]. (You can paginate through more pages by adding a page param if needed, since the API might have many results. Here we requested 50 per page which is the max in one call.)

## 4. Chronicling America API – Search historical newspapers by keyword

This function queries the Chronicling America collection for a keyword in a date range. It returns JSON

results of newspaper pages that match. Note: The LOC API doesn't require a key. We use the collection-specific endpoint with `fo=json`. The query uses `qs` (query string) and date filters.

⬇
import requests

def search_chronicling_america(query, start_year, end_year):
"""
Search Chronicling America newspapers for the query between start_year and end_year.
Returns JSON results (newspaper pages matching the query).
"""
base_url = "<https://www.loc.gov/collections/chronicling-america/>"
params = {
"fo": "json",
"start_date": f"{start_year}-01-01",
"end_date": f"{end_year}-12-31",
"qs": query

# You could add other filters like state or specific newspaper if desired

}
response = requests.get(base_url, params=params)
response.raise_for_status()
return response.json()

Usage: search_chronicling_america("moon landing", 1960, 1970) might find newspaper pages from the 1960s referencing “moon landing”. The JSON will list page results with metadata. (Since Chronicling America’s coverage largely stops at 1963, in this example you’d get results primarily up to ’63.) Each result may include a snippet of OCR text where the term appears. If you want the full page text, you would use the provided resource URLs (the JSON may contain a URL to the page image and OCR text). The function as given provides the search capability within the given date range.

## 5 GDELT Events Query – Filter events by date (and optional keyword)

For GDELT, there isn’t a simple REST query for arbitrary keywords, so our approach will be to fetch the data files and filter. Below is a function that demonstrates how you might retrieve GDELT events for a given date range (year range) and filter by a keyword in the actor names. This uses direct file download for illustration. (For real use, if the query is complex, you’d likely use BigQuery with an SQL query.) We keep this example straightforward and use Python’s CSV handling. Note that downloading large files can be slow, so this approach is best for limited ranges or specific filters.

⬇
import csv
import requests
from io import BytesIO
from zipfile import ZipFile

def fetch_gdelt_events(start_year, end_year, keyword=None):

"""
Fetch GDELT v1 events from start_year to end_year.
If keyword is provided, filter events where Actor1Name or Actor2Name contains the keyword (case-insensitive).
Returns a list of event records (as dicts).
"""
events = []
base_url = "<http://data.gdeltproject.org/events/>"

# Loop through each year in range

for year in range(start_year, end_year + 1):
file_url = f"{base_url}{year}.zip"
resp = requests.get(file_url)
resp.raise_for_status()

# Open the zip file from bytes

with ZipFile(BytesIO(resp.content)) as z:

# Each yearly zip contains a CSV (tab-separated) named like {year}.export.CSV or similar

for filename in z.namelist():
if filename.endsWith(".CSV") or filename.endsWith(".csv"):
with z.open(filename) as csvfile:
reader = csv.reader(TextIOWrapper(csvfile,
errors=’ignore’), delimiter=’\t’)
for row in reader:

# GDELT v1 columns (per codebook) – simplified for demo

# e.g.: GlobalEventID, Date, Actor1Name, Actor2Name, EventCode, GoldsteinScale, SourceURL, etc

if keyword:

# simple case-insensitive substring match in actor names

actor1 = row[6]

# assuming Actor1Name is column 6

actor2 = row[16]

# assuming Actor2Name is column 16

if keyword.lower() in actor1.lower() or keyword.lower() in actor2.lower():
events.append(row)
else:
events.append(row)
return events

```

### Usage:

`events = fetch_gdelt_events(2010, 2012, keyword="Russia")` would download GDELT event files for 2010, 2011, 2012 and collect events where either actor name contains “Russia”. Each `row` in the result corresponds to a GDELT event record (with fields like date, actors, event type, etc.). In a real scenario, you might want to convert each row to a dictionary with field names using the GDELT schema. Also, for large data ranges, you’d consider streaming or using pandas chunk processing to handle memory.

This example is primarily to show how one could map the query parameters to the dataset retrieval: since GDELT is not a queryable API in the same way, we either filter client-side or run a BigQuery SQL. (Using BigQuery, the equivalent would be a SQL `WHERE Year BETWEEN start_year AND end_year AND Actor1Name CONTAINS 'keyword'`. That approach is often more efficient for large-scale filtering.)

# Archive Lookup Fallback Function

Finally, for any URLs we get from Google or Bing (or even NYT/GDELT source URLs), we should retrieve an archived version to guard against link rot. Here's a simple helper that generates a Wayback Machine lookup URL for a given page URL. This URL can be used to see archived copies or trigger a new archive capture:

```python
def get_archive_url(original_url):
""
Given an original URL, return a web.archive.org lookup URL that shows its archived history.
""
return f"https://web.archive.org/web/*/{original_url}"
```

Usage: If Google returned a result <http://example.com/old-article>., calling get_archive_url("<http://example.com/old-article>.") would give "<https://web.archive.org/web/*/http://example.com/old-article>." Visiting this link shows the Wayback Machine timeline of that page (all archived snapshots). You could refine it further (for instance, to automatically retrieve the oldest or newest snapshot via the Wayback CDX API), but providing the timeline link is a straightforward way to allow a user or script to then pick a snapshot.

Alternatively, if you wanted to automatically get the latest archived version, you could use the Wayback "availability" API. For example:

```python
import requests
def getlatest_archive(original_url): api  $=$  "http://archive.org/wayback/available" resp  $=$  requests.get(api,params  $\coloneqq$  {"url":original_url}) data  $=$  resp.json() snap  $=$  data.get("archived_snapshots",{}).get("closest") if snap: return snap["url"] # direct link to the closest archived page return None
```

This would return the URL of the latest archived snapshot if available (or None if not archived yet). For simplicity, our get_archive_url above just constructs the general lookup address, which is often sufficient.

With these functions in our toolkit, we can: search historical news on NYT and The Guardian (with full text for analysis in Guardian's case), search historic newspapers via Chronicling America, fetch global event data

via GDELT, find any web page via Google/Bing, and then use the archive to retrieve the content of pages that might be gone or paywalled. All of this using strictly free resources and respecting the date constraints needed for 1990–2012 content and beyond.

1 14 15 16 Using the loc.gov API with the Chronicling America Historic Newspapers Collection — Tutorials for Data Exploration
<https://libraryofcongress.github.io/data-exploration/loc.gov%20JSON%20API/Chronicling_America/README.html>

2 File search
<https://superscape.org/filesearch/>

3 4 How to download archived content from the Wayback Machine : r/DataHoarder
<https://www.reddit.com/r/DataHoarder/comments/10udrh8/how_to_download_archived_content_from_the_wayback/>

5 Historical analysis of NYT using web API - Kohei Watanabe
<https://blog.koheiw.net/?p=643>

6 Working with the NY Times API - RPubs
<https://rpubs.com/aliceafriedman/week-9-HW>

7 New York Times - Text and Data Mining Databases
<https://guides.library.georgetown.edu/c.php?g=729844&amp;p=9706817>

8 The Guardian - Open Platform
<https://open-platform.theguardian.com/>

9 10 12 13 The Guardian - Open Platform - Get Started
<https://open-platform.theguardian.com/access/>

11 documentation / content - theguardian / open platform
<https://open-platform.theguardian.com/documentation/search>

17 18 21 22 Data: Querying, Analyzing and Downloading: The GDELT Project
<https://www.gdeltproject.org/data.html>

19 The Datasets Of GDELT As Of February 2016 – The GDELT Project
<https://blog.gdeltproject.org/the-datasets-of-gdelt-as-of-february-2016/>

20 GDELT Project - Wikipedia
<https://en.wikipedia.org/wiki/GDELT_Project>

23 Developing a Strategic Early Warning System to predict and monitor ...
<https://medium.com/thedeephub/developing-a-strategic-early-warning-system-to-predict-and-monitor-global-crisis-part-i-b32e25f769ac>

24 [PDF] An investigation of the effectiveness of using Twitter data for ...
<https://repository.up.ac.za/server/api/core/bitstreams/677ad071-f961-4f13-b7b3-eb3504a101cc/content>

25 26 27 28 29 Custom Search JSON API | Programmable Search Engine | Google for Developers
<https://developers.google.com/custom-search/v1/overview>

30 32 33 Exploring the Bing Date Search Operators
<https://nullhandle.org/blog/2024-06-12-exploring-the-bing-date-search-operators.html>

31 Bing "before", "after" and "Custom Range Date" doesn't work. - Reddit

<https://www.reddit.com/r/bing/comments/zhh2g9/bing_before_after_and_custom_range_date_doesnt/>
