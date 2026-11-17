# Anti-bot handling (Scrapling 0.5)

Use this for reliable, authorized automation. Inspect responses before
escalating: a successful HTTP status can still contain a challenge or login page.

## Escalation

1. Start with `Fetcher` or `FetcherSession` for HTML/API data. Reuse connections
   and cookies, lower concurrency, add crawl delays and honor retry signals.
2. Use `StealthyFetcher` or `StealthySession` when JavaScript is required.
   Scrapling 0.5 removed the separate `DynamicFetcher` / `DynamicSession` backend.
   Prefer a specific `wait_selector` when the required content is known;
   `network_idle=True` can help but does not prove extraction is complete.
3. For an authorized Cloudflare-protected target, opt into
   `solve_cloudflare=True`. This attempts challenge handling; it is not a
   guarantee of success. Reuse a browser session for related requests.
4. Use approved proxies only where required; see [proxy rotation](proxy-rotation.md).
   Persisting authentication with a fixed proxy may be preferable to rotation.

## Browser example

Browser timeouts are milliseconds. Per-fetch options go on `fetch()` here;
browser-wide choices such as `headless` go on session creation.

```python
from scrapling.fetchers import StealthySession

with StealthySession(headless=True) as session:
    page = session.fetch(
        "https://example.com", solve_cloudflare=True, network_idle=True,
        timeout=60000, google_search=False,
    )
    print(page.status, page.css("title::text").get())
```

Validate target fields as well as status/title. Stop and report unresolved
blocks rather than presenting a challenge page as the requested data. Capture
only the HTML or screenshot needed for diagnosis; exclude credentials and
private session state from output. Avoid disabling resources that the login or
content flow needs.

Do not bypass authentication or paywalls without permission, or scrape sensitive
personal data. Follow the target site's access and rate-limit rules.
