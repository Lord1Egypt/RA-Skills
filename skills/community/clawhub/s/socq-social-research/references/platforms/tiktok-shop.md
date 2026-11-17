# TikTok Shop

Generated from SocQ Capability Registry schema `v1-9a87cca161f6`. Read this file when the request targets TikTok Shop.

## Endpoint selection

| Endpoint | Use for | Input choice | Standard schema | Cost |
| --- | --- | --- | --- | --- |
| [`tiktok-shop/product`](https://docs.socq.ai/api-manual/tiktok-shop/product) | TikTok Shop Product API | url | `product@1.0` | 0.7 credits/result |
| [`tiktok-shop/product-reviews`](https://docs.socq.ai/api-manual/tiktok-shop/product-reviews) | TikTok Shop Product Reviews API | url | `review@1.0` | 0.3 credits/result |
| [`tiktok-shop/products`](https://docs.socq.ai/api-manual/tiktok-shop/products) | TikTok Shop Products API | url | `product@1.0` | 0.7 credits/result |
| [`tiktok-shop/search`](https://docs.socq.ai/api-manual/tiktok-shop/search) | TikTok Shop Search API | query | `product@1.0` | 0.7 credits/result |
| [`tiktok-shop/user-showcase`](https://docs.socq.ai/api-manual/tiktok-shop/user-showcase) | TikTok Shop User Showcase API | username | `product@1.0` | 0.7 credits/result |

## Validated examples

### `tiktok-shop/product`

Typed MCP tool: `socq_tiktok_shop_product`

This endpoint currently supports US only. Omit region or set it to US; other regions are rejected before task creation.

```json
{
  "url": "https://www.tiktok.com/shop/pdp/example-product/1234567890123456789"
}
```

### `tiktok-shop/product-reviews`

Typed MCP tool: `socq_tiktok_shop_product_reviews`

```json
{
  "url": "https://www.tiktok.com/shop/pdp/example-product/1234567890123456789"
}
```

### `tiktok-shop/products`

Typed MCP tool: `socq_tiktok_shop_products`

```json
{
  "url": "https://www.tiktok.com/shop/store/example-store/1234567890123456789"
}
```

### `tiktok-shop/search`

Typed MCP tool: `socq_tiktok_shop_search`

```json
{
  "query": "wireless earbuds"
}
```

### `tiktok-shop/user-showcase`

Typed MCP tool: `socq_tiktok_shop_user_showcase`

This endpoint currently supports US only. Omit region or set it to US; other regions are rejected before task creation. results_limit must be 20 to 2000.

```json
{
  "username": "example_creator"
}
```
