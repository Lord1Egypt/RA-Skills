---
name: scavio-walmart
description: Search Walmart products and look up product details by product ID. Supports delivery speed, ZIP code, and in-store availability filters. Returns structured JSON.
version: 2.0.3
tags: walmart, retail, product-search, ecommerce, price-lookup, shopping, agents, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 90
    throttle: 1
    emoji: "\U0001F3EA"
    homepage: https://scavio.dev/docs
---

# Walmart Product Search via Scavio

Search Walmart products or retrieve full product details by product ID. Returns structured JSON with pricing, ratings, fulfillment, and availability.

## When to trigger

Use this skill when the user asks to:
- Find products on Walmart with price or delivery requirements
- Check same-day or next-day availability for a product near a ZIP code
- Look up a specific Walmart product by product ID
- Compare Walmart prices (pair with scavio-amazon for cross-retailer comparison)
- Filter products by in-store pickup availability

## Setup

Get a free API key at https://scavio.dev (250 free credits/month, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

## Workflow

1. If the user has a Walmart product ID, call `/api/v1/walmart/product` directly.
2. If the user has a keyword, call `/api/v1/walmart/search`.
3. If the user asks about delivery speed (e.g. "can I get this today?"), set `fulfillment_speed` and `delivery_zip`.
4. If the user asks about in-store pickup, set `fulfillment_type: in_store` and `store_id` if known.
5. Present results with name, price, rating, fulfillment info, and product URL.

## Endpoints

| Endpoint | Description |
|---|---|
| `POST https://api.scavio.dev/api/v1/walmart/search` | Keyword search with filters |
| `POST https://api.scavio.dev/api/v1/walmart/product` | Full product details by product ID |

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Search Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search query (1-500 chars) |
| `sort_by` | string | `best_match` | `best_match`, `price_low`, `price_high`, `best_seller` |
| `start_page` | integer | `1` | Starting page |
| `min_price` | integer | -- | Minimum price filter (dollars) |
| `max_price` | integer | -- | Maximum price filter (dollars) |
| `fulfillment_speed` | string | -- | `today`, `tomorrow`, `2_days`, `anytime` |
| `fulfillment_type` | string | -- | `in_store` for click-and-collect |
| `delivery_zip` | string | -- | ZIP code for localized results |
| `store_id` | string | -- | Walmart store ID for in-store availability |
| `device` | string | `desktop` | `desktop`, `mobile`, or `tablet` |

## Product Detail Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | Walmart product ID |
| `delivery_zip` | string | -- | ZIP code for localized pricing |
| `store_id` | string | -- | Walmart store ID |

## Examples

```python
import os, requests

BASE = "https://api.scavio.dev"
HEADERS = {"Authorization": f"Bearer {os.environ['SCAVIO_API_KEY']}"}

# Search with delivery filter
results = requests.post(f"{BASE}/api/v1/walmart/search", headers=HEADERS,
    json={"query": "standing desk", "sort_by": "best_seller", "max_price": 300,
          "fulfillment_speed": "tomorrow", "delivery_zip": "10001"}).json()

# Product by ID
product = requests.post(f"{BASE}/api/v1/walmart/product", headers=HEADERS,
    json={"product_id": "123456789", "delivery_zip": "10001"}).json()
```

## Search Response

```json
{
  "data": [
    {
      "name": "Flexispot Standing Desk",
      "product_id": "123456789",
      "url": "https://www.walmart.com/ip/123456789",
      "price": "$249.00",
      "was_price": "$349.99",
      "rating": 4.7,
      "total_reviews": 8230,
      "fulfillment": "Free shipping",
      "in_stock": true,
      "seller": "Walmart.com"
    }
  ],
  "credits_used": 1,
  "credits_remaining": 999
}
```

Product detail response also includes: `description`, `features`, `images`, `categories`, `availability`, `fulfillment`.

## Guardrails

- Never fabricate product names, prices, product IDs, or availability. Only return data from the API.
- If the user asks about delivery to a specific location, always pass `delivery_zip` — availability varies by ZIP.
- `fulfillment_speed: today` results are time-sensitive; mention this to the user.
- Always include the product URL so the user can verify and complete purchase.

## Failure handling

- If no products are returned, relax filters (remove `fulfillment_speed` or increase `max_price`) and retry.
- If the product ID is not found, suggest a keyword search instead.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## LangChain

```bash
pip install langchain-scavio
```

```python
from langchain_scavio import ScavioSearchTool
tool = ScavioSearchTool(engine="walmart")
```
