# SERP / Google-Compatible Search

Raw `google.com/search` can return Google verification, consent, or JavaScript retry pages when accessed through proxy traffic. For public SERP research, use the SDK SERP preset instead of scraping raw Google directly.

## Recommended Python usage

```python
from iploop import IPLoop

ip = IPLoop("YOUR_API_KEY", country="US")
results = ip.serp.search("public search query", country="US")
print(results["results"])
```

## Google compatibility wrapper

```python
ip.google.search("public search query", country="US")
```

`ip.google.search(...)` uses the SERP-safe path by default. If you need raw Google for QA only:

```python
ip.google.search("public search query", country="US", direct=True)
```

Raw mode may return zero results or a verification page. Treat it as diagnostics, not the production SERP path.

## Response shape

```json
{
  "success": true,
  "source": "startpage",
  "country": "US",
  "count": 10,
  "results": [
    {
      "title": "Example result",
      "url": "https://example.com/",
      "snippet": "..."
    }
  ]
}
```

## Fallback behavior

The SERP preset uses:

1. Startpage-backed Google-compatible SERP path
2. DuckDuckGo HTML fallback

This avoids exposing users to raw Google verification pages for normal public SERP research.

## Proxy auth reminder

Canonical proxy auth is:

```text
username: iploop
password: YOUR_API_KEY-country-US
host: proxy.iploop.io
port: 8880
```

curl example:

```bash
curl --proxy "http://proxy.iploop.io:8880" \
  --proxy-user "iploop:${IPLOOP_API_KEY}-country-US" \
  https://httpbin.org/ip
```
