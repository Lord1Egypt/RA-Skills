# Parsing and browser recipes (Scrapling 0.5)

## CSS, XPath and first/all matches

Fetch results expose the same selection methods as a standalone `Selector`.

```python
from scrapling import Selector

page = Selector('<div class="quote"><span class="text">Hello</span></div><a href="/next">Next</a>')
quotes = page.css(".quote .text::text").getall()
links = page.css("a::attr(href)").getall()
first_quote = page.xpath('//span[@class="text"]/text()').get()
```

## Next.js JSON

Select by script ID instead of assuming attribute order in an HTML regex.
`__NEXT_DATA__` is optional; many newer Next.js pages use other data sources.

```python
import json
from scrapling import Selector

page = Selector('<script type="application/json" id="__NEXT_DATA__">{"props":{"pageProps":{"title":"Example"}}}</script>')
raw = page.css("script#__NEXT_DATA__::text").get()
next_data = json.loads(raw) if raw else None
props = next_data.get("props", {}).get("pageProps", {}) if next_data else {}
```

## Adaptive selection

Enable adaptive storage before saving or relocating a selector. Reuse the same
URL/storage context and selector identifier across runs. Validate relocated
content; relocation is not proof that a redesign was handled correctly.

```python
from scrapling.fetchers import Fetcher

Fetcher.configure(adaptive=True)
page = Fetcher.get("https://example.com/products")
products = page.css(".product", auto_save=True)

# On a later run, after the DOM changed:
page = Fetcher.get("https://example.com/products")
products = page.css(".product", adaptive=True)
```

For session-based fetching, pass `selector_config={"adaptive": True}` when
creating the response. Adaptive selectors are a Python parser feature, not a
separate adaptive CSS/XPath MCP tool.

## Scroll before extracting

`fetch()` returns a parsed `Response`, not an interactive page. A `page_action`
callback operates on the Patchright page before response capture. Bound the
scroll and adapt waits to the site's actual loading behavior.

```python
from scrapling.fetchers import StealthyFetcher


def scroll_page(page):
    for _ in range(3):
        page.mouse.wheel(0, 1200)
        page.wait_for_timeout(500)


if __name__ == "__main__":
    response = StealthyFetcher.fetch(
        "https://example.com/items", headless=True, page_action=scroll_page
    )
    print(response.css(".item::text").getall())
```

## Authorized login in a session

Adapt selectors and the success condition to the real login flow. Use one tab
for this flow. Credentials are read at runtime; never commit or print them.

```python
import os
from scrapling.fetchers import StealthySession


def login(page):
    page.fill('input[name="username"]', os.environ["SCRAPE_USERNAME"])
    page.fill('input[name="password"]', os.environ["SCRAPE_PASSWORD"])
    page.click('button[type="submit"]')
    page.wait_for_url("**/dashboard")


if __name__ == "__main__":
    with StealthySession(headless=True, max_pages=1) as session:
        session.fetch("https://example.com/login", page_action=login)
        dashboard = session.fetch("https://example.com/dashboard")
        print(dashboard.css("h1::text").get())
```

## Spider exports

After defining a concrete spider, run `result = MySpider().start()` and then
`result.items.to_jsonl("out.jsonl")` or `result.items.to_json("out.json")`.
See [spider recipes](spider-recipes.md) for complete classes and async streaming.
