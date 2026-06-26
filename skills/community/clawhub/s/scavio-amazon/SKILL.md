---
name: scavio-amazon
description: Search Amazon products and look up product details by ASIN. Returns structured JSON with price, rating, Prime status, and availability. Supports 12 Amazon marketplaces.
version: 2.0.3
tags: amazon, product-search, ecommerce, asin, price-lookup, shopping, agents, langchain, crewai, autogen, structured-data, json, ai-agents, retail
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "\U0001F6D2"
    homepage: https://scavio.dev/docs
---

# Amazon Product Search via Scavio

Search Amazon products or retrieve full product details by ASIN. Returns structured JSON. Supports 12 Amazon marketplaces.

## When to trigger

Use this skill when the user asks to:
- Find products on Amazon with price or rating requirements
- Look up a specific product by ASIN
- Research Amazon pricing, availability, or reviews
- Compare Amazon products or find best sellers in a category

## Setup

Get a free API key at https://scavio.dev (250 free credits/month, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

## Workflow

1. If the user has an ASIN, call `/api/v1/amazon/product` directly.
2. If the user has a keyword, call `/api/v1/amazon/search` with appropriate filters (`sort_by`, `domain`, `zip_code`).
3. If the user asks about a specific market (e.g. "Amazon Germany"), set the `domain` param accordingly.
4. Present results with name, price, rating, review count, and URL. Note Prime status.

## Endpoints

| Endpoint | Description |
|---|---|
| `POST https://api.scavio.dev/api/v1/amazon/search` | Keyword search with filters |
| `POST https://api.scavio.dev/api/v1/amazon/product` | Full product details by ASIN |

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Search Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search query (1-500 chars) |
| `domain` | string | `com` | `com`, `co.uk`, `de`, `fr`, `co.jp`, `ca`, `it`, `es`, `in`, `com.au`, `com.br`, `com.mx` |
| `sort_by` | string | -- | `most_recent`, `price_low_to_high`, `price_high_to_low`, `featured`, `average_review`, `bestsellers` |
| `start_page` | integer | `1` | Starting page |
| `pages` | integer | `1` | Number of pages |
| `category_id` | string | -- | Amazon category/department ID |
| `currency` | string | -- | ISO 4217 (e.g. `USD`, `EUR`) |
| `zip_code` | string | -- | ZIP code for localized pricing and availability |
| `device` | string | `desktop` | `desktop`, `mobile`, or `tablet` |

## Product Detail Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Amazon ASIN (e.g. `B09XS7JWHH`) |
| `domain` | string | `com` | Amazon domain suffix |
| `currency` | string | -- | ISO 4217 currency code |
| `zip_code` | string | -- | ZIP code for localized pricing |

## Examples

```python
import os, requests

BASE = "https://api.scavio.dev"
HEADERS = {"Authorization": f"Bearer {os.environ['SCAVIO_API_KEY']}"}

# Search
results = requests.post(f"{BASE}/api/v1/amazon/search", headers=HEADERS,
    json={"query": "wireless headphones", "sort_by": "average_review"}).json()

# Product by ASIN
product = requests.post(f"{BASE}/api/v1/amazon/product", headers=HEADERS,
    json={"query": "B09XS7JWHH"}).json()
```

## Search Response

```json
{
  "data": [
    {
      "name": "Sony WH-1000XM5 Wireless Noise Canceling Headphones",
      "asin": "B09XS7JWHH",
      "url": "https://www.amazon.com/dp/B09XS7JWHH",
      "price": "$278.00",
      "currency": "USD",
      "rating": 4.6,
      "total_reviews": 12450,
      "is_prime": true,
      "is_best_seller": false
    }
  ],
  "credits_used": 1,
  "credits_remaining": 999
}
```

Product detail response also includes: `description`, `features`, `images`, `categories`, `availability`, `seller`, `list_price`.

## Guardrails

- Never fabricate product names, ASINs, prices, or ratings. Only return data from the API.
- If the user asks for a price comparison, search both terms and present both results.
- If an ASIN is not found, tell the user and suggest a keyword search instead.
- Always include the product URL so the user can verify.

## Failure handling

- If the API returns an error, report the status code and stop.
- If no products are returned, tell the user and suggest different keywords or filters.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## LangChain

```bash
pip install langchain-scavio
```

```python
from langchain_scavio import ScavioSearchTool
tool = ScavioSearchTool(engine="amazon")
```
