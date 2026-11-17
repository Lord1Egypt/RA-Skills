# Spider recipes (Scrapling 0.5)

Adapt domains and selectors before running these independent examples. Use
`Spider.start()` from synchronous code; inside an event loop consume
`spider.stream()` for asynchronous item processing. Examples enable
robots.txt handling. Session retries and spider `max_blocked_retries` are distinct;
Scrapy's `custom_settings` is not a Scrapling configuration interface.

## Product extraction and pagination

```python
from datetime import datetime, timezone
from urllib.parse import urljoin
from scrapling.spiders import Spider, Response


class ProductSpider(Spider):
    name = "products"
    start_urls = ["https://shop.example.com/products"]
    concurrent_requests = 5
    download_delay = 2.0
    robots_txt_obey = True
    max_blocked_retries = 3

    async def parse(self, response: Response):
        for product in response.css(".product-card"):
            href = product.css("a::attr(href)").get()
            yield {
                "name": product.css(".product-name::text").get(),
                "price": product.css(".price::text").get(),
                "rating": product.css(".rating::attr(data-score)").get(),
                "url": urljoin(response.url, href) if href else None,
                "extracted_at": datetime.now(timezone.utc).isoformat(),
            }
        next_page = response.css(".pagination .next::attr(href)").get()
        if next_page:
            yield response.follow(next_page)


if __name__ == "__main__":
    ProductSpider(crawldir="./crawl_products").start().items.to_jsonl("products.jsonl")
```

## Sitemap crawl

The built-in template handles sitemap indexes, XML namespaces and gzip. With no
rules, sitemap page URLs go to the overridden `parse()` method.

```python
from scrapling.spiders import SitemapSpider, Response


class PageSitemapSpider(SitemapSpider):
    name = "sitemap_pages"
    sitemap_urls = ["https://example.com/sitemap.xml"]
    robots_txt_obey = True

    async def parse(self, response: Response):
        yield {"url": response.url, "title": response.css("h1::text").get()}


if __name__ == "__main__":
    PageSitemapSpider().start().items.to_jsonl("pages.jsonl")
```

## API-first pagination

Schedule the next page only after receiving nonempty results. Returning from
an async generator stops that branch; raising `StopIteration` is an error.
Configure authorized API credentials through the existing secret mechanism.

```python
from scrapling.spiders import Spider, Request, Response


class APISpider(Spider):
    name = "api_products"
    api_base = "https://api.example.com/v1"
    max_pages = 100
    robots_txt_obey = True

    async def start_requests(self):
        yield Request(f"{self.api_base}/products?page=1", meta={"page": 1})

    async def parse(self, response: Response):
        products = response.json()["products"]
        if not products:
            return
        for product in products:
            yield product
        page = response.meta["page"]
        if page < self.max_pages:
            yield response.follow(
                f"{self.api_base}/products?page={page + 1}",
                meta={"page": page + 1},
            )
```

## Multiple domains and handlers

```python
from urllib.parse import urlparse
from scrapling.spiders import Spider, Response


class MultiDomainSpider(Spider):
    name = "multi"
    start_urls = ["https://shop.example.com/", "https://blog.example.com/"]
    robots_txt_obey = True
    domain_handlers = {"shop.example.com": "parse_shop", "blog.example.com": "parse_blog"}

    async def parse(self, response: Response):
        handler_name = self.domain_handlers.get(urlparse(response.url).hostname)
        if handler_name is None:
            self.logger.warning("No handler for %s", response.url)
            return
        async for item in getattr(self, handler_name)(response):
            yield item

    async def parse_shop(self, response):
        for product in response.css(".product"):
            yield {"type": "product", "title": product.css("h2::text").get()}

    async def parse_blog(self, response):
        for article in response.css("article"):
            yield {"type": "article", "title": article.css("h1::text").get()}
```

## Stream items

```python
import asyncio
from scrapling.spiders import Spider, Response


class StreamingSpider(Spider):
    name = "streaming"
    start_urls = ["https://example.com/items"]
    robots_txt_obey = True

    async def parse(self, response: Response):
        for item in response.css(".item"):
            yield {"id": item.attrib.get("data-id"),
                   "content": item.css(".content::text").get()}


async def main():
    async for item in StreamingSpider().stream():
        print(item)


if __name__ == "__main__":
    asyncio.run(main())
```

## Bounded link crawl

Depth is explicit request metadata in this plain Spider example. Restrict hosts;
a depth limit alone does not bound the number of URLs. Add a project-specific
URL/page budget before running a large crawl.

```python
from urllib.parse import urljoin, urlparse
from scrapling.spiders import Spider, Response


class DeepCrawlSpider(Spider):
    name = "deep_crawl"
    start_urls = ["https://example.com/"]
    depth_limit = 3
    robots_txt_obey = True

    async def parse(self, response: Response):
        depth = response.meta.get("depth", 0)
        yield {"url": response.url, "depth": depth,
               "title": response.css("title::text").get()}
        if depth >= self.depth_limit:
            return
        for href in response.css("a::attr(href)").getall():
            url = urljoin(response.url, href)
            if (urlparse(url).scheme in {"http", "https"}
                    and urlparse(url).hostname == "example.com"):
                yield response.follow(url, meta={"depth": depth + 1})
```

## Form submission

Use `Request(method="POST", data=...)`; Scrapling has no `FormRequest` class.
Fetch and parse CSRF fields first when the authorized form requires them.

```python
from scrapling.spiders import Spider, Request, Response


class FormSpider(Spider):
    name = "form_search"
    robots_txt_obey = True

    async def start_requests(self):
        for keyword in ["python", "scraping", "data"]:
            yield Request("https://example.com/search", method="POST",
                          data={"q": keyword, "category": "all"}, meta={"keyword": keyword})

    async def parse(self, response: Response):
        for result in response.css(".search-result"):
            yield {"keyword": response.meta["keyword"],
                   "title": result.css("h3::text").get(),
                   "snippet": result.css(".snippet::text").get()}
```

## Image/media download

Create the output directory and derive filenames locally rather than trusting
remote paths. This example accepts only HTTP(S) images on the starting host.

```python
import hashlib
from pathlib import Path
from urllib.parse import urljoin, urlparse
from scrapling.spiders import Spider, Response


class MediaSpider(Spider):
    name = "media"
    start_urls = ["https://example.com/gallery"]
    download_dir = Path("./downloads")
    robots_txt_obey = True

    async def parse(self, response: Response):
        for src in response.css("img::attr(src)").getall():
            url = urljoin(response.url, src)
            if (urlparse(url).scheme not in {"http", "https"}
                    or urlparse(url).hostname != "example.com"):
                continue
            suffix = Path(urlparse(url).path).suffix.lower()
            if suffix not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
                suffix = ".bin"
            filename = hashlib.sha256(url.encode()).hexdigest() + suffix
            yield response.follow(url, callback=self.save_image, meta={"filename": filename})

    async def save_image(self, response: Response):
        if response.status != 200:
            self.logger.warning("Download failed: %s (%s)", response.url, response.status)
            return
        self.download_dir.mkdir(parents=True, exist_ok=True)
        path = self.download_dir / response.meta["filename"]
        path.write_bytes(response.body)
        yield {"downloaded": str(path)}
```

## Pause/resume and failures

Pass the same `crawldir` to a new instance of the same spider after a graceful
Ctrl+C pause. Use a new checkpoint directory for a fresh crawl instead of
deleting unknown state. Do not mix checkpoints across changed request identity,
spider scope or incompatible versions.

Log and skip a missing optional field when appropriate. Let unexpected
exceptions surface through the spider's error reporting rather than swallowing
every exception and treating partial output as a successful full crawl. Check
result statistics and failed requests against the crawl's acceptance criteria.
