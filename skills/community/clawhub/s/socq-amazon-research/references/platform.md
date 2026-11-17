# Amazon

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets Amazon.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`amazon/best-sellers`](https://docs.socq.ai/api-manual/amazon/best-sellers) | Collect public Amazon best sellers. | urls | `product@1.0` | 0.15 credits/result |
| [`amazon/product-detail`](https://docs.socq.ai/api-manual/amazon/product-detail) | Collect public Amazon product details. | urls | `product@1.0` | 0.15 credits/result |
| [`amazon/product-search`](https://docs.socq.ai/api-manual/amazon/product-search) | Search public Amazon products. | domain, query | `product@1.0` | 0.15 credits/result |
| [`amazon/reviews`](https://docs.socq.ai/api-manual/amazon/reviews) | Collect public Amazon reviews. | urls | `review@1.0` | 0.15 credits/result |
| [`amazon/seller-info`](https://docs.socq.ai/api-manual/amazon/seller-info) | Collect public Amazon seller information. | urls | `seller@1.0` | 0.15 credits/result |

## Validated examples

### `amazon/best-sellers`

Typed MCP tool: `socq_amazon_best_sellers`

```json
{
  "urls": [
    "https://www.amazon.com/Best-Sellers-Books/zgbs/books"
  ],
  "results_limit": 3
}
```

### `amazon/product-detail`

Typed MCP tool: `socq_amazon_product_detail`

```json
{
  "urls": [
    "https://www.amazon.com/dp/B0CHHSFMRL"
  ]
}
```

### `amazon/product-search`

Typed MCP tool: `socq_amazon_product_search`

```json
{
  "query": "wireless earbuds",
  "domain": "https://www.amazon.com",
  "results_limit": 3
}
```

### `amazon/reviews`

Typed MCP tool: `socq_amazon_reviews`

```json
{
  "urls": [
    "https://www.amazon.com/dp/B0CHHSFMRL"
  ],
  "results_limit": 3
}
```

### `amazon/seller-info`

Typed MCP tool: `socq_amazon_seller_info`

```json
{
  "urls": [
    "https://www.amazon.com/sp?seller=A2L77EE7U53NWQ"
  ]
}
```
