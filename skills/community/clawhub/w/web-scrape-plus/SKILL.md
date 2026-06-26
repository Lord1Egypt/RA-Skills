---
name: web-scrape-plus
description: "Enhanced web scraping with anti-detection, proxy support, rate limiting, data validation, and multiple extraction methods. Supports static pages, dynamic content, login-gated sites, and pagination."
metadata:
  author: opencode
  version: 2.0
  tags: web-scraping, data-extraction, anti-detection, proxy
  compatibility: opencode
  license: MIT
---

# Web Scrape Plus

Enhanced web scraping with anti-detection, proxy support, rate limiting, and data validation.

## Features

- **Multiple Extraction Methods**: Static HTML, dynamic DOM, API endpoints
- **Anti-Detection**: User agent rotation, random delays, fingerprint evasion
- **Proxy Support**: HTTP/SOCKS5 proxy routing
- **Rate Limiting**: Configurable request throttling
- **Data Validation**: Schema validation and deduplication
- **Error Recovery**: Retry logic with exponential backoff

## Approach Selection

| Scenario | Method | Tool |
|----------|--------|------|
| Static HTML | CSS/XPath selectors | web_fetch |
| Dynamic content | Browser automation | browser |
| API endpoints | Direct HTTP requests | http-client |
| Login required | Session management | browser + cookies |
| Pagination | Sequential/parallel | browser + loops |

## Anti-Detection Techniques

### User Agent Rotation

```python
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
]

headers = {"User-Agent": random.choice(USER_AGENTS)}
```

### Random Delays

```python
import time
import random

def random_delay(min_sec=1, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))
```

### Viewport Randomization

```python
VIEWPORTS = [
    {"width": 1920, "height": 1080},
    {"width": 1366, "height": 768},
    {"width": 1536, "height": 864},
]

viewport = random.choice(VIEWPORTS)
```

## Proxy Support

```python
import requests

proxies = {
    "http": "http://proxy:port",
    "https": "http://proxy:port",
}

response = requests.get(url, proxies=proxies)
```

## Rate Limiting

```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window
        self.timestamps = deque()
    
    def wait_if_needed(self):
        now = time.time()
        while self.timestamps and self.timestamps[0] < now - self.time_window:
            self.timestamps.popleft()
        if len(self.timestamps) >= self.max_requests:
            sleep_time = self.timestamps[0] + self.time_window - now
            if sleep_time > 0:
                time.sleep(sleep_time)
        self.timestamps.append(time.time())
```

## Error Recovery

```python
import time
from functools import wraps

def retry(max_retries=3, backoff_factor=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    wait_time = backoff_factor ** attempt
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator
```

## Data Validation

```python
from pydantic import BaseModel, validator
from typing import List, Optional

class ScrapedItem(BaseModel):
    title: str
    url: str
    price: Optional[float]
    description: Optional[str]
    
    @validator("title")
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("title cannot be empty")
        return v.strip()

def validate_items(items: List[dict]) -> List[ScrapedItem]:
    return [ScrapedItem(**item) for item in items]
```

## Deduplication

```python
def deduplicate(items, key="url"):
    seen = set()
    unique = []
    for item in items:
        item_key = item.get(key)
        if item_key not in seen:
            seen.add(item_key)
            unique.append(item)
    return unique
```

## Workflow

1. **Test one page first** - Verify extraction works
2. **Choose method** - Static vs dynamic vs API
3. **Apply anti-detection** - User agents, delays, proxies
4. **Rate limit** - Respect server limits
5. **Validate data** - Schema validation
6. **Deduplicate** - Remove duplicates
7. **Save results** - JSON/CSV output
8. **Cleanup** - Close browsers, clear state

## Best Practices

1. **Respect robots.txt** - Check before scraping
2. **Rate limit** - Don't overload servers
3. **Use proxies** - Rotate IPs for large jobs
4. **Validate data** - Ensure quality
5. **Handle errors** - Retry logic
6. **Cache responses** - Avoid re-fetching
7. **Log requests** - Debug issues
8. **Clean up** - Close browsers, clear state

## Common Issues

| Issue | Solution |
|-------|----------|
| CAPTCHA | Switch proxy, use manual solving |
| Rate limited | Increase delays, rotate proxies |
| Dynamic content | Use browser automation |
| Login required | Use session cookies |
| Anti-bot detection | Use stealth mode |

## Output Formats

### JSON

```json
[
  {
    "title": "...",
    "url": "...",
    "price": 29.99,
    "description": "..."
  }
]
```

### CSV

```csv
title,url,price,description
"Product 1",https://example.com/1,29.99,"Description 1"
```
