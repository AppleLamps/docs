# Quick Reference Guide - Historical APIs Toolkit

**Date:** January 2026 | **Coverage:** 1990–2012 research

---

## 🚀 One-Command Setup

```bash
pip install requests google-cloud-bigquery
```

---

## 5 APIs at a Glance

### 1. Internet Archive CDX ✅ BEST FOR: Web snapshots

```python
cdx = InternetArchiveCDX()
results = cdx.query("example.com", 1990, 2012)
```

**Why:** Only source for complete web history (1996+)  
**Cost:** Free, unlimited | **Auth:** None  
**Link Rot:** ✅ Zero risk | **30-Day Trap:** ✅ Safe

---

### 2. New York Times Article Search ✅ BEST FOR: Quality US news

```python
nyt = NYTArticleSearch(api_key="YOUR_KEY")
articles = nyt.iterate_all_results("climate change", 1990, 2012)
```

**Why:** Highest-quality structured content (1851+)  
**Cost:** Free (4K/day) | **Auth:** API key (5 min setup)  
**Link Rot:** ✅ Low risk | **30-Day Trap:** ✅ Safe

Get key: https://developer.nytimes.com/

---

### 3. Chronicling America ✅ BEST FOR: Historic newspapers (1690–1963)

```python
ca = ChroniclingAmerica()
results = ca.query("Civil War", 1860, 1865)
```

**Why:** ONLY source for 1690–1963 full-text  
**Cost:** Free, unlimited | **Auth:** None  
**Link Rot:** ✅ Zero risk | **30-Day Trap:** ✅ Safe

---

### 4. GDELT BigQuery ✅ BEST FOR: Global event data

```python
gdelt = GDELTBigQuery("path/to/keyfile.json")
events = gdelt.query_events(1990, 2012, event_codes=["0211"])
```

**Why:** 35+ years of structured newsflow (1979+)  
**Cost:** Free (1TB/month) | **Auth:** Google Cloud  
**Link Rot:** ⚠️ Source links may rot | **30-Day Trap:** ⚠️ Minimal

**Setup:** 30 min via https://console.cloud.google.com

---

### 5. The Guardian API ✅ BEST FOR: International perspective (1999+)

```python
guardian = GuardianAPI(api_key="YOUR_KEY")
articles = guardian.iterate_all_results("world bank", 1999, 2012)
```

**Why:** Non-US viewpoint, generous free tier, fast  
**Cost:** Free (1M/month!) | **Auth:** API key (5 min setup)  
**Link Rot:** ✅ Low risk | **30-Day Trap:** ✅ Safe  
**Limitation:** No coverage before 1999 ❌

Get key: https://open-platform.theguardian.com/

---

## 🎯 Decision Tree: Which API to Use?

```
Is your query about...?

1. SPECIFIC TIME PERIOD?
   ├─ Before 1690? → Not in any API
   ├─ 1690–1963?  → Chronicling America (only source!)
   ├─ 1963–1999?  → Internet Archive CDX + GDELT
   ├─ 1999–2012?  → CDX + NYT + GDELT + Guardian
   └─ 2012+?      → All APIs work

2. LOOKING FOR FULL-TEXT?
   ├─ Yes → Chronicling America (newspapers) or Archive snapshots
   └─ No  → NYT snippets, GDELT metadata, Guardian abstracts

3. NEED STRUCTURED ANALYSIS?
   ├─ Yes → GDELT BigQuery (SQL queries)
   └─ No  → CDX, NYT, Guardian (article-based)

4. BUDGET?
   ├─ $0, no setup → CDX, Chronicling America
   ├─ $0, 5-min setup → NYT, Guardian (API keys)
   └─ $0, 30-min setup → GDELT BigQuery (Google Cloud)
```

---

## 📊 Coverage Map

```
Time Period | CDX | NYT | CA  | GDELT | Guardian
─────────────────────────────────────────────────
1690–1836   |  ✗  |  ✗  | ✓✓✓ |   ✗   |    ✗
1836–1922   |  ✗  |  ✗  | ✓✓✓ |   ✗   |    ✗
1922–1963   |  ✗  |  ✗  | ✓✓✓ |   ✗   |    ✗
1963–1979   |  ◐  |  ◐  |  ✗  |   ✗   |    ✗
1979–1996   |  ◐  |  ✓  |  ✗  |  ✓✓✓  |    ✗
1996–1999   | ✓✓  |  ✓  |  ✗  |  ✓✓✓  |    ✗
1999–2012   | ✓✓✓ |  ✓  |  ✗  |  ✓✓✓  |   ✓✓
2012–now    | ✓✓✓ | ✓✓✓ |  ✗  |  ✓✓✓  |  ✓✓✓

Legend: ✗ = No | ◐ = Sparse | ✓ = Good | ✓✓ = Excellent | ✓✓✓ = Complete
```

---

## ⚡ Quick Commands Reference

### Search by keyword + date range

```python
# Single API
results = nyt.query("9/11", 2001, 2001)

# Multiple APIs
orchestrator = HistoricalNewsOrchestrator(nyt_key="...", guardian_key="...")
results = orchestrator.comprehensive_search("climate", 1990, 2012)
```

### Check web archive coverage

```python
captures = cdx.query("example.com", 1990, 2012)
print(f"Found {len(captures['captures'])} snapshots")
```

### Get permanent archive link

```python
url = cdx.build_wayback_url("example.com", "20010911")
# Output: https://web.archive.org/web/20010911/http://example.com
```

### Fallback to archive when link dies

```python
fallback = ArchiveOrgFallback()
archive_url = fallback.get_closest_snapshot("deadlink.com", 2005)
```

---

## 🚨 "30-Day Trap" Prevention

### What It Is
Google/Bing re-index the web. Old pages that no one links to disappear from search results.

### How This Toolkit Avoids It
| API | Strategy |
|-----|----------|
| **CDX** | Archives static (never re-indexed) |
| **NYT** | Indexes own archive (not live web) |
| **CA** | Library of Congress (permanent) |
| **GDELT** | Events timestamped at publication |
| **Guardian** | Their archive (not live web) |

✅ **All recommended APIs are safe from the 30-Day Trap**

---

## 📈 Response Times

| API | Time | Notes |
|-----|------|-------|
| **CDX** | <1 sec | Instant |
| **NYT** | 1–5 sec | REST API |
| **CA** | <1 sec | Instant |
| **GDELT BigQuery** | 5–30 sec | SQL query |
| **Guardian** | <1 sec | Instant |

---

## 💾 Data Export

### To CSV
```python
import csv
with open("results.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=['date', 'title', 'url'])
    writer.writeheader()
    writer.writerows(articles)
```

### To JSON
```python
import json
with open("results.json", "w") as f:
    json.dump(articles, f, indent=2)
```

### To Pandas DataFrame
```python
import pandas as pd
df = pd.DataFrame(articles)
df.to_csv("results.csv", index=False)
```

---

## 🔑 API Keys Needed

| API | Required? | Get Here |
|-----|-----------|----------|
| CDX | ❌ No | None |
| NYT | ✅ Yes | https://developer.nytimes.com/ |
| CA | ❌ No | None |
| GDELT v1 | ❌ No | None |
| GDELT BigQuery | ✅ Yes | https://console.cloud.google.com |
| Guardian | ✅ Yes | https://open-platform.theguardian.com/ |

**Total setup time:** 30 minutes

---

## ✅ Sanity Check Your Query

- [ ] Date range: 1690–2012 ✓
- [ ] API supports your time period ✓
- [ ] API key valid (if required) ✓
- [ ] Query text is reasonable (1–5 keywords) ✓
- [ ] Rate limits respected (delays added) ✓
- [ ] Response format understood (JSON/CSV) ✓
- [ ] Results exported/saved ✓

---

## 🆘 Troubleshooting in 30 Seconds

| Problem | Solution |
|---------|----------|
| "Connection timeout" | Increase delay: `rate_limit_delay=2.0` |
| "API key invalid" | Verify key in web console, ensure API enabled |
| "No results" | Check date range supported, try different query |
| "Too many requests" | Add delays: `rate_limit_delay=2.0` |
| "BigQuery auth error" | Verify service account has BigQuery User role |
| "Link returns 404" | Use: `fallback.get_closest_snapshot(url, year)` |

---

## 📚 Next Steps

1. **Install:** `pip install requests google-cloud-bigquery`
2. **Pick API:** Use decision tree above
3. **Get keys:** Register for free keys (5 min each)
4. **Run example:** Copy code matching your API
5. **Iterate:** Adjust date range, query terms
6. **Export:** Save results to CSV/JSON

---

**Status:** ✅ Production-ready | **Python:** 3.7+ | **License:** MIT

