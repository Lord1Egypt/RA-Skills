---
name: Web Scraper (r.jina.ai)
description: Bypass Cloudflare and scrape any website using r.jina.ai API. Works on sites with strong protection like Truth Social, Cloudflare Turnstile, etc.
version: "1.0.0"
author: Liuge
tags:
  - web
  - scraper
  - cloudflare
  - bypass
  - jina
---

# Web Scraper using r.jina.ai

Bypass Cloudflare and scrape any website using free r.jina.ai API.

## Features

- Bypass Cloudflare, Turnstile, and other protections
- Works on Truth Social, Bitget, and other protected sites
- Returns clean Markdown content
- Free to use

## Usage

Simply prepend `https://r.jina.ai/` to any URL:

```
https://r.jina.ai/https://truthsocial.com/@realDonaldTrump
https://r.jina.ai/https://bitget.com/events/poolx
```

## Examples

### Get Trump Truth Social posts:
```
curl -s "https://r.jina.ai/https://truthsocial.com/@realDonaldTrump"
```

### Get any protected page:
```
curl -s "https://r.jina.ai/https://example.com"
```

## In Code

```python
import requests

def scrape(url):
    return requests.get(f"https://r.jina.ai/{url}").text
```

## Use Cases

- Scrape Truth Social, Gab, Gettr
- Bypass Cloudflare protected sites
- Extract content from news articles
- Monitor competitors
