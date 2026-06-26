# Scrapling — Full Reference

## CLI Commands

```
scrapling extract get             # HTTP GET (static sites)
scrapling extract fetch           # Browser automation (JS-heavy)
scrapling extract stealthy-fetch  # Stealth browser (anti-bot / Cloudflare)
scrapling extract post            # HTTP POST
scrapling extract put             # HTTP PUT
scrapling extract delete          # HTTP DELETE
```

## Shared Options (all HTTP commands)

| Option | Description |
|--------|-------------|
| `-s, --css-selector TEXT` | Extract only matching elements |
| `-H, --headers TEXT` | HTTP headers (repeatable): `"Key: Value"` |
| `--cookies TEXT` | Cookies: `"name=val; name2=val2"` |
| `--timeout INTEGER` | Timeout in seconds (default: 30) |
| `--proxy TEXT` | `http://user:pass@host:port` |
| `-p, --params TEXT` | Query params: `"key=value"` (repeatable) |
| `--impersonate TEXT` | Browser to impersonate: `Chrome`, `Firefox`, `Safari` |
| `--stealthy-headers` | Use browser-like headers (default: on) |

## Browser Options (fetch / stealthy-fetch)

| Option | Description |
|--------|-------------|
| `--network-idle` | Wait for network to go idle after load |
| `--wait INTEGER` | Extra wait in ms after page load |
| `--wait-selector TEXT` | CSS selector to wait for before proceeding |
| `--headless / --no-headless` | Headless mode (default: on) |
| `--disable-resources` | Drop images/fonts for speed |
| `--real-chrome` | Use installed Chrome instead of bundled |

## stealthy-fetch Only

| Option | Description |
|--------|-------------|
| `--solve-cloudflare` | Attempt to solve Cloudflare challenges |
| `--block-webrtc` | Block WebRTC |
| `--hide-canvas` | Add canvas noise |
| `--allow-webgl / --block-webgl` | WebGL toggle (default: allow) |

## Output Formats

| Extension | Output |
|-----------|--------|
| `.md` | HTML → Markdown (best for reading) |
| `.txt` | Clean plain text |
| `.html` | Raw HTML |
| `.json` | JSON (for API responses) |

## Spider Framework (Python)

```python
from scrapling.spiders import Spider, Request, Response

class MySpider(Spider):
    name = "my_spider"
    start_urls = ["https://example.com/"]
    concurrent_requests = 10

    async def parse(self, response: Response):
        for item in response.css('.item'):
            yield {"title": item.css('h2::text').get()}
        next_page = response.css('.next a')
        if next_page:
            yield response.follow(next_page[0].attrib['href'])

result = MySpider().start()
result.items.to_json("output.json")
```

Pause/resume:
```python
MySpider(crawldir="./crawl_data").start()
# Ctrl+C to pause, restart with same crawldir to resume
```

## Python Fetcher API

```python
from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher

# Static
page = Fetcher.get('https://example.com/')

# Dynamic (JS)
page = DynamicFetcher.fetch('https://example.com/', network_idle=True)

# Stealth / Cloudflare
page = StealthyFetcher.fetch('https://example.com/', solve_cloudflare=True)

# Parse
quotes = page.css('.quote .text::text').getall()
author = page.css('.author::text').get()
links = page.css('a::attr(href)').getall()

# XPath
items = page.xpath('//div[@class="item"]/text()').getall()

# Navigation
siblings = page.css('.item')[0].find_similar()
parent = page.css('.item')[0].parent
```

## Session Persistence

```python
from scrapling.fetchers import FetcherSession

with FetcherSession(impersonate='chrome') as session:
    page1 = session.get('https://example.com/login')
    # session cookies persist automatically
    page2 = session.get('https://example.com/dashboard')
```

## Docker

```bash
docker pull pyd4vinci/scrapling
docker run pyd4vinci/scrapling extract get "https://example.com" output.md
```
