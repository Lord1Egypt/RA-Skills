# API Reference

## EchoTik API (Influencer Data)

**Endpoint:** `GET https://open.echotik.live/api/v3/echotik/influencer/list`

### Headers

| Header | Required | Value |
|--------|----------|-------|
| `Authorization` | Yes | `Basic <base64(user:pass)>` |
| `Content-Type` | Yes | `application/json` |

### Query Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page_size` | int | 10 | Results per page (max 10) |
| `page_num` | int | 1 | Page number (1-based) |
| `region` | string | US | Market code: US, SG, TH, UK, etc. |

### Response Schema

```json
{
  "code": 0,
  "message": "success",
  "data": [
    {
      "nick_name": "username",
      "total_followers_cnt": 12345,
      "interaction_rate": 0.082,
      "ec_score": 4.5,
      "sales": 500,
      "avg_30d_price": 15.99,
      "category": "[]",
      "avg_view_cnt": 50000
    }
  ]
}
```

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `nick_name` | string | Display name |
| `total_followers_cnt` | int | Follower count |
| `interaction_rate` | float | Engagement rate (0.08 = 8%) |
| `ec_score` | float | E-commerce score (0-10) |
| `sales` | int | Lifetime sales count |
| `avg_30d_price` | float | Avg product price (USD) |

### Credential Setup

1. Register at https://www.echotik.com/
2. Generate API credentials
3. Encode: `echo -n "username:password" | base64`
4. Set: `export ECHOTIK_AUTH_HEADER="Basic <encoded>"`

---

## TikTok Shop Partner API (Product Data)

**Endpoint:** `GET https://api.tiktokshop.com/v2/products/search`

### Authentication

TikTok Shop API uses OAuth 2.0. First obtain an access token:

```bash
curl -X POST "https://auth.tiktokshop.com/api/v2/oauth/token" \
  -H "Content-Type: application/json" \
  -d '{
    "app_key": "YOUR_APP_KEY",
    "app_secret": "YOUR_APP_SECRET",
    "grant_type": "client_credentials"
  }'
```

### Headers

| Header | Required | Value |
|--------|----------|-------|
| `Authorization` | Yes | `Bearer <access_token>` |
| `Content-Type` | Yes | `application/json` |

### Query Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `category_id` | int | — | Category ID (10001=beauty, 10002=3c, etc.) |
| `region` | string | — | Market code: US, SG, TH, etc. |
| `sort_by` | string | gmv_growth | Sort: gmv_growth / sales_volume / created_time |
| `page_size` | int | 20 | Results per page |
| `page_number` | int | 1 | Page number |

### Response Schema

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "products": [
      {
        "product_id": "123456",
        "title": "Product Name",
        "category_id": 10002,
        "sales_volume": 25800,
        "gmv": 258000,
        "price": 10.0,
        "gmv_growth": "+67%",
        "image_url": "https://..."
      }
    ],
    "total": 1000,
    "page_number": 1,
    "page_size": 20
  }
}
```

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `product_id` | string | Unique product ID |
| `title` | string | Product title |
| `category_id` | int | Category ID |
| `sales_volume` | int | Total sales count |
| `gmv` | int | Gross merchandise value (cents) |
| `price` | float | Price (USD) |
| `gmv_growth` | string | GMV growth rate (e.g. "+67%") |

### Credential Setup

1. Log in to https://seller.tiktokglobalshop.com/
2. Go to **Developer Center** → **App Management**
3. Create an app and obtain **App Key** and **App Secret**
4. Use OAuth endpoint to get access_token
5. Set: `export TIKTOK_SHOP_API_KEY="your_access_token"`

### Notes

- Access tokens expire. Refresh periodically.
- API rate limits apply. Respect rate limits.
- Product data availability varies by region and seller permissions.
- Without `TIKTOK_SHOP_API_KEY`, the script skips product fetching gracefully.

---

## Category ID Mapping

| Category | ID |
|----------|-----|
| Beauty | 10001 |
| 3C Electronics | 10002 |
| Home & Living | 10003 |
| Fashion | 10004 |
| Food & Beverage | 10005 |
| Sports & Outdoors | 10006 |
| Baby & Maternity | 10007 |
| Pet Supplies | 10008 |
