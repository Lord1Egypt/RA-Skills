# Proxy rotation (Scrapling 0.5)

Use authorized proxy infrastructure when the task requires it. Reduce request
rate and honor server retry signals before escalating. A proxy is not permission
to access restricted content. Use current provider documentation instead of a
hard-coded sponsor/provider list.

## Rotator and sessions

`ProxyRotator` is exported from `scrapling.fetchers`. Default rotation is cyclic
round-robin. `get_proxy()` manually selects the next proxy; use a session's
`proxy_rotator` argument for automatic per-request selection.

```python
from scrapling.fetchers import FetcherSession, ProxyRotator

rotator = ProxyRotator([
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
])
print(rotator.get_proxy())  # Manual selection; no network request.

if __name__ == "__main__":
    with FetcherSession(proxy_rotator=rotator) as session:
        page = session.get("https://example.com")
        print(page.status)
```

Do not combine `proxy_rotator` with session-level `proxy` or `proxies`.
Credentials belong in the existing secret mechanism, not committed code or logs.
Browser rotation uses a separate context per proxy; do not assume login state
is shared across rotating contexts. Use an authorized fixed proxy when session
affinity is required.

## Spider integration

Configure the rotator through the supplied session manager, rather than
mutating a nonexistent `self.sessions` dictionary between responses.

```python
from scrapling.fetchers import FetcherSession, ProxyRotator
from scrapling.spiders import Spider, Response


class RotatingSpider(Spider):
    name = "rotating"
    start_urls = ["https://example.com/"]
    download_delay = 2.0
    robots_txt_obey = True
    max_blocked_retries = 3

    def configure_sessions(self, manager):
        rotator = ProxyRotator([
            "http://proxy1.example.com:8080",
            "http://proxy2.example.com:8080",
        ])
        manager.add("default", FetcherSession(proxy_rotator=rotator))

    async def parse(self, response: Response):
        yield {"url": response.url, "title": response.css("title::text").get()}
```

## Custom strategy

The `strategy` argument is a callable, not a string such as `"cyclic"`. Its
signature is `(proxies, current_index) -> (selected_proxy, next_index)`.

```python
import random
from scrapling.fetchers import ProxyRotator


def random_strategy(proxies, current_index):
    index = random.randrange(len(proxies))
    return proxies[index], index


rotator = ProxyRotator(
    ["http://proxy1.example.com:8080", "http://proxy2.example.com:8080"],
    strategy=random_strategy,
)
```

Test proxies with a small authorized request before a full crawl. Track response
status and failures without exposing credential-bearing URLs.
