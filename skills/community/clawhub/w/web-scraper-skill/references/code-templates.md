# Code Templates: Apify & Firecrawl

## Firecrawl — Python

### Scrape a Single Page
```python
import requests

API_KEY = "fc-YOUR_API_KEY"

response = requests.post(
    "https://api.firecrawl.dev/v2/scrape",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "url": "https://example.com",
        "formats": ["markdown"],
        "onlyMainContent": True,
    }
)
data = response.json()
if data["success"]:
    print(data["data"]["markdown"])
```

### Crawl a Website (Async + Poll)
```python
import requests, time

API_KEY = "fc-YOUR_API_KEY"
BASE = "https://api.firecrawl.dev/v2"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Start crawl
resp = requests.post(f"{BASE}/crawl", headers=HEADERS, json={
    "url": "https://docs.example.com",
    "limit": 50,
    "scrapeOptions": {"formats": ["markdown"]}
})
job_id = resp.json()["id"]

# Poll until done
while True:
    status = requests.get(f"{BASE}/crawl/{job_id}", headers=HEADERS).json()
    if status["status"] == "completed":
        pages = status["data"]
        break
    elif status["status"] == "failed":
        raise Exception("Crawl failed")
    time.sleep(5)

for page in pages:
    print(page["metadata"]["sourceURL"], page["markdown"][:100])
```

### Search + Scrape
```python
resp = requests.post(f"{BASE}/search", headers=HEADERS, json={
    "query": "best Python web scraping libraries 2025",
    "limit": 5,
    "scrapeOptions": {"formats": ["markdown"]}
})
for result in resp.json()["data"]:
    print(result["title"], result["url"])
    print(result.get("markdown", "")[:200])
```

---

## Firecrawl — JavaScript (Node.js)

```javascript
const API_KEY = "fc-YOUR_API_KEY";
const BASE = "https://api.firecrawl.dev/v2";

// Scrape
const res = await fetch(`${BASE}/scrape`, {
  method: "POST",
  headers: { "Authorization": `Bearer ${API_KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({ url: "https://example.com", formats: ["markdown"], onlyMainContent: true })
});
const data = await res.json();
console.log(data.data.markdown);
```

---

## Apify — Python

### Run Actor and Get Results (using apify-client)
```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")

# Run Google Search Scraper
run = client.actor("apify/google-search-scraper").call(run_input={
    "queries": "web scraping tools",
    "maxPagesPerQuery": 1,
    "resultsPerPage": 10,
})

# Fetch results
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Raw HTTP (no SDK)
```python
import requests, time

TOKEN = "YOUR_APIFY_TOKEN"
ACTOR = "apify/google-search-scraper"
BASE = "https://api.apify.com/v2"

# Start run
resp = requests.post(
    f"{BASE}/acts/{ACTOR}/runs",
    params={"token": TOKEN},
    json={"queries": "web scraping", "maxPagesPerQuery": 1}
)
run = resp.json()["data"]
run_id = run["id"]
dataset_id = run["defaultDatasetId"]

# Poll status
while True:
    status = requests.get(f"{BASE}/acts/{ACTOR}/runs/{run_id}", params={"token": TOKEN}).json()
    if status["data"]["status"] in ("SUCCEEDED", "FAILED"):
        break
    time.sleep(5)

# Fetch dataset
items = requests.get(f"{BASE}/datasets/{dataset_id}/items", params={"token": TOKEN, "format": "json"}).json()
for item in items:
    print(item)
```

### Synchronous Run (short jobs <5 min)
```python
resp = requests.post(
    f"{BASE}/acts/{ACTOR}/run-sync-get-dataset-items",
    params={"token": TOKEN},
    json={"queries": "Jaipur restaurants", "maxPagesPerQuery": 1}
)
items = resp.json()  # Direct list of results
```

---

## Apify — JavaScript

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });

// Run and wait
const run = await client.actor('compass/crawler-google-places').call({
  searchStringsArray: ['coffee shops in Jaipur'],
  maxCrawledPlaces: 10,
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

---

## Save Results to File (Python)

```python
import json

# After getting items from either API
with open("results.json", "w") as f:
    json.dump(items, f, indent=2, ensure_ascii=False)
print(f"Saved {len(items)} items to results.json")
```
