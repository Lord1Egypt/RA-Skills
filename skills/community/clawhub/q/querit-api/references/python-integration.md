# Python integration

## SDK or REST?

Use the official SDK for search. Use REST for `needContent`, `chunksPerDoc`, and `/v1/contents`.

```bash
pip install querit   # GitHub: querit-ai/querit-python
python3 -c "import querit; print(querit.__version__)"   # confirm the install
```

```python
import os

from querit import QueritClient
from querit.models.request import SearchRequest, SearchFilters, SiteFilter, GeoFilter
from querit.errors import QueritError

client = QueritClient(api_key=os.environ["QUERIT_API_KEY"], timeout=30)

request = SearchRequest(
    query="quantum computing breakthroughs",
    count=10,
    filters=SearchFilters(
        languages=["english"],                          # or Language.ENGLISH
        sites=SiteFilter(include=["arxiv.org"]),        # exclude=[...] also supported
        geo=GeoFilter(countries=["united states"]),     # or Country.UNITED_STATES
        time_range="d7",                                # or "w2" / "m3" / "y1" / "2026-08-01to2026-08-10"
    ),
)

try:
    response = client.search(request)
    for item in response.results:
        print(item.title, item.url)
except QueritError as exc:
    print(f"Search failed: {exc}")
```

SDK surface (v0.1.4):

- `filters` takes a `SearchFilters` dataclass. `SearchFilters.to_dict()` emits `languages.include`, `geo.countries.include`, `sites.include` / `sites.exclude`, and `timeRange.date`.
- Enum values are lowercase full names, not ISO codes. `Language`: `english`, `japanese`, `korean`, `german`, `french`, `spanish`, `portuguese`. `Country`: `united states`, `united kingdom`, `south korea`, `india`, `japan`, `germany`, `france`, `spain`, `brazil`, `mexico`, `canada`, `australia`, `argentina`, `colombia`, `indonesia`, `nigeria`, `philippines`. Anything outside the enum raises `ValueError` before the request is sent, so `"US"` raises `Unsupported country: US`.
- `SearchRequest` takes `query`, `count`, and `filters`, and `QueritClient` targets `/v1/search`. Page text, multi-chunk summaries, and the contents endpoint go through REST.
- The client reuses a pooled session with one retry for connection errors and read timeouts, and does not retry on HTTP status codes. Rate limiting is still the caller's job.
- Error classes: `QueritAPIError`, `QueritAuthError`, `QueritValidationError`, all under `QueritError`. Reuse one client instance rather than constructing one per call.

On the response side, `SearchResponse.results` unwraps the `results.result` nesting and yields `SearchResultItem` objects exposing `url`, `title`, `snippet`, and `page_age`, with `error_code`, `error_msg`, and `search_id` on the response. `item.raw` is the underlying dict, which is where fields without a dedicated property live:

```python
sentences = item.raw.get("sentence") or []
site = item.raw.get("site_name")
```

## A REST client for search options and contents

Needed for `needContent`, `chunksPerDoc`, and `/v1/contents`. QPS is plan-dependent, so batch work needs a limiter rather than relying on retries to absorb 429s. The class is named `QueritRestClient` so it can coexist with the SDK's `QueritClient` in the same project.

```python
import os
import random
import threading
import time

import requests

SEARCH_URL = "https://api.querit.ai/v1/search"
CONTENTS_URL = "https://api.querit.ai/v1/contents"
RETRYABLE = {429, 500, 502, 503, 504}


class QueritRestClient:
    """Shared connection pool, QPS limiter, bounded retries."""

    def __init__(self, api_key=None, qps=1.0, timeout=20, max_retries=3):
        key = api_key or os.environ.get("QUERIT_API_KEY")
        if not key:
            raise RuntimeError("QUERIT_API_KEY is not set")
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        self._min_interval = 1.0 / qps if qps > 0 else 0.0
        self._timeout = timeout
        self._max_retries = max_retries
        self._lock = threading.Lock()
        self._next_slot = 0.0

    def _throttle(self):
        # Serialize departures so concurrent workers respect the account QPS.
        with self._lock:
            now = time.monotonic()
            wait = max(0.0, self._next_slot - now)
            self._next_slot = max(now, self._next_slot) + self._min_interval
        if wait:
            time.sleep(wait)

    def _post(self, url, payload):
        last_error = None
        for attempt in range(self._max_retries + 1):
            self._throttle()
            try:
                resp = self._session.post(url, json=payload, timeout=self._timeout)
            except requests.RequestException as exc:
                last_error = exc
            else:
                if resp.status_code not in RETRYABLE:
                    resp.raise_for_status()
                    return resp.json()
                last_error = requests.HTTPError(f"HTTP {resp.status_code}", response=resp)
            if attempt < self._max_retries:
                # Jitter keeps concurrent workers from retrying in lockstep.
                time.sleep((2 ** attempt) * 0.5 + random.uniform(0, 0.3))
        raise last_error

    def search(self, query, count=10, need_content=False, filters=None):
        payload = {"query": query, "count": count, "needContent": need_content}
        if filters:
            payload["filters"] = filters
        return self._post(SEARCH_URL, payload)

    def contents(self, urls, fmt="markdown", crawl_timeout=10, extras_meta=True):
        if not 1 <= len(urls) <= 10:
            raise ValueError("contents accepts 1-10 URLs per call")
        return self._post(CONTENTS_URL, {
            "urls": list(urls),
            "format": fmt,
            "crawlTimeout": crawl_timeout,
            "extrasMeta": extras_meta,
        })
```

Set `qps` to match the account, not what the machine can push. Keep `timeout` above `crawlTimeout` on contents calls.

`filters` here is the raw nested dict, since there is no dataclass to build it:

```python
body = client.search(
    "quantum computing breakthroughs",
    count=10,
    need_content=True,
    filters={
        "languages": {"include": ["english"]},
        "geo": {"countries": {"include": ["united states"]}},
        "timeRange": {"date": "d7"},
        "sites": {"include": ["arxiv.org"]},
    },
)
```

## Batch contents with chunking

```python
from concurrent.futures import ThreadPoolExecutor


def chunked(seq, size=10):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


def fetch_all(client, urls, workers=4):
    pages, failures = [], []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        batches = list(chunked(urls, 10))
        for batch, body in zip(batches, pool.map(client.contents, batches)):
            status_by_id = {s.get("id"): s.get("status") for s in body.get("statuses", [])}
            seen = set()
            for item in body.get("results", []):
                url = item.get("url")
                seen.add(url)
                if status_by_id.get(item.get("id")) == "success":
                    pages.append({"url": url, "text": item.get("content") or ""})
                else:
                    failures.append(url)
            # A URL absent from results entirely is also a failure.
            failures.extend(u for u in batch if u not in seen)
    return pages, failures
```

Return failures alongside successes. Swallowing them turns a partial crawl into a quality problem with no trail back to the failed fetch.

## Normalizing search results for RAG

```python
def normalize_search(body):
    docs = []
    for item in body.get("results", {}).get("result", []):
        sentences = item.get("sentence") or []   # absent means "no page text"
        docs.append({
            "url": item.get("url"),
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "site": item.get("site_name"),
            "age": item.get("page_age"),
            "text": " ".join(sentences),
            "has_text": bool(sentences),
        })
    return docs
```

Carry `has_text` explicitly: it lets a caller fall back to `/v1/contents` for that URL, and it makes text coverage measurable when tuning `needContent` against a two-call pipeline.

Every field in a result is optional, so read them with `.get()` throughout rather than indexing - `item["sentence"]` raises `KeyError` on a result that simply has no page text, which is a normal response, not an error.

## Logging and secret hygiene

- Log `search_id` and `took` on every call.
- Never log the `Authorization` header. If the project logs request headers wholesale, add a redaction filter first.
- Read the key from the environment or a secret manager, not from source, notebooks, or a committed `.env`.
