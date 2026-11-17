# Scrapling 0.5 API reference

These examples target >=0.5,<0.6. Use the installed version's signatures if a
later series changes the API. MCP tools are distinct from these Python APIs;
see [MCP setup](mcp-setup.md).

## Fetchers and responses

```python
from scrapling.fetchers import Fetcher, StealthyFetcher

page = Fetcher.get("https://example.com", timeout=30)
# For JavaScript-rendered pages:
page = StealthyFetcher.fetch(
    "https://example.com", headless=True, timeout=30000, wait_selector="h1"
)
```

`FetcherSession` supports reusable sync/async HTTP. `StealthySession` and
`AsyncStealthySession` provide browser reuse. DynamicFetcher/DynamicSession
were removed in 0.5. HTTP timeouts are seconds; browser timeouts are milliseconds.

A response exposes `status`, `url`, `html_content`, `body`, `json()`, `css()`
and `xpath()`. It is parsed response content, not a browser Page. Prefer
`.css("h1::text").get()` for a first match, `.getall()` for all matches.

## Browser interaction

Pass a callback receiving the live Patchright Page through `page_action`:

```python
from scrapling.fetchers import StealthySession

def load_more(page):
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_selector(".item")

with StealthySession(headless=True) as session:
    response = session.fetch("https://example.com/items", page_action=load_more)
    items = response.css(".item::text").getall()
```

This illustrates one scroll, not a complete infinite-scroll crawler. Bound any
repeated scrolling and wait for newly loaded items rather than assuming a sleep
proves completion. Login callbacks similarly call `fill`/`click` on the live
Page and wait for an authenticated state; subsequent requests through the same
session reuse cookies. Do not call these methods on a fetched Response. Use an
async callback with `AsyncStealthySession`.

## Parser navigation and adaptive matching

```python
from scrapling import Selector

page = Selector('<div class="product"><h2>Widget</h2></div>', adaptive=True)
products = page.css(".product", auto_save=True)
first = products[0]
parent = first.parent
children = first.children
below = first.below_elements
similar = first.find_similar()
```

`below_elements` is a property. Generated selector properties are
`first.generate_css_selector` and `first.generate_xpath_selector`; consult the parser API before invoking
methods. There are no `auto_css_selector()` or `auto_xpath()` methods.
For fetched pages, initialize the fetcher's parser through
`selector_config={"adaptive": True}` before saving/retrieving fingerprints.
Use a stable URL/identifier and persistent storage for relocation across runs.
See [recipes](recipes.md) for an example. Adaptive matching is heuristic;
verify extracted values after a page redesign.

## Spiders and proxies

Import `Spider`, `Request`, `Response` from `scrapling.spiders`.
`start_requests()` and item-producing callbacks are async generators. Form
submissions use `Request(url, method="POST", data={...})`, not `FormRequest`.
Use `max_blocked_retries` for Spider blocked-response retry limits, and session
`retries`/`retry_delay` for request retries; `custom_settings` is not a Scrapling
settings mechanism. See [spider recipes](spider-recipes.md).

Import `ProxyRotator` from `scrapling.fetchers`; its default strategy rotates
round-robin. `.get_proxy()` returns a proxy; `proxy_rotator=rotator` on a session
enables per-request rotation. A custom `strategy` is callable, not the string
`"cyclic"`. See [proxy rotation](proxy-rotation.md).
