---
name: vigilath-shopping
description: Search, bargain, order, and pay for pet supplies on Vigilath.com — an AI-powered pet commerce platform with multi-round price negotiation.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - VIGILATH_TOKEN
      bins:
        - curl
    primaryEnv: VIGILATH_TOKEN
---

# Vigilath.com Pet Commerce

You can search products, negotiate prices, place orders, and pay on Vigilath.com (an AI pet supplies marketplace).

## Base URL

All endpoints use: `https://www.vigilath.com`

## Authentication

Every API call (except auth endpoints) requires:
```
Authorization: Bearer $VIGILATH_TOKEN
```

### Getting a token

If `VIGILATH_TOKEN` is not set, use Device Flow to obtain one:

1. Create session:
```bash
curl -s -X POST https://www.vigilath.com/api/agent/auth/session \
  -H "Content-Type: application/json" -d '{}'
```
Response: `{"sessionId": "...", "authUrl": "https://www.vigilath.com/api/agent/auth/page?code=XXX-123", "code": "XXX-123", "expiresIn": 600}`

2. Show the `authUrl` to the user and ask them to open it in a browser to log in.

3. Poll for token (every 5 seconds, up to 10 minutes):
```bash
curl -s -X POST https://www.vigilath.com/api/agent/auth/token \
  -H "Content-Type: application/json" -d '{"sessionId": "SESSION_ID"}'
```
- HTTP 428: user hasn't logged in yet, keep polling
- HTTP 200: `{"accessToken": "eyJ...", "expiresIn": 2592000}` — save this as VIGILATH_TOKEN
- HTTP 410: session expired, start over

Token is valid for 30 days.

## Capabilities

### 1. Smart Shopping (search + AI selection)

```bash
curl -s -X POST https://www.vigilath.com/api/agent/shopping \
  -H "Authorization: Bearer $VIGILATH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "organic dog food for small breeds", "language": "English"}'
```

Response contains `selected_products` (array) and `natural_message` (AI recommendation).

Each product includes: `spuId`, `spuName`, `priceFee` (cents CNY), `mainImgUrl`, `selling_point`, `categoryName`, `skuId`, `shopId`, `shopName`, `stock`, `bargain_enabled`.

Products with `bargain_enabled: true` support price negotiation (see Bargain below).

### 2. Bargain (multi-round price negotiation)

For products with `bargain_enabled: true`, you can negotiate a lower price.

**Step 1** — Search with bargain mode:
```bash
curl -s -X POST https://www.vigilath.com/api/agent/shopping \
  -H "Authorization: Bearer $VIGILATH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "dog food", "bargain": true}'
```
Response includes `bargain_sessions` with `sessionId` for each bargain-enabled product.

**Step 2** — Send counter-offers:
```bash
curl -s -X POST https://www.vigilath.com/api/agent/bargain \
  -H "Authorization: Bearer $VIGILATH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "SESSION_ID", "message": "I offer 25 yuan"}'
```

Response:
```json
{
  "sessionId": "...",
  "productName": "Premium Dog Food",
  "originalPrice": 35.0,
  "currentPrice": 30.0,
  "message": "25 is too low! How about 30?",
  "round": 2,
  "dealReached": false,
  "isActive": true,
  "quote": null
}
```

**Step 3** — Repeat until `dealReached: true`. The response will include a `quote`:
```json
{
  "dealReached": true,
  "quote": {
    "quoteId": "q_xyz789",
    "bargainPrice": 30.0,
    "discount": 5.0,
    "expiresAt": "2026-04-02T12:00:00"
  }
}
```

**Step 4** — Place order with `quoteId` to apply bargain price (see Order below).

Supported messages: counter-offer ("25块", "I'll pay 80"), accept ("deal", "成交"), quit ("算了", "quit"), leverage ("competitor is cheaper", "I'm a loyal customer").

### 3. Place Order

```bash
curl -s -X POST https://www.vigilath.com/api/agent/order \
  -H "Authorization: Bearer $VIGILATH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"items": [{"spuId": 12345, "quantity": 1}], "addrId": null, "quoteId": null}'
```

- `items`: array of `{spuId, quantity}` — skuId/shopId auto-resolved from spuId
- `addrId`: shipping address ID, or `null` to use user's default address
- `quoteId`: bargain quote ID from a successful negotiation (optional)

Response: `{"data": {"order_number": "...", "total": 2999, "status": "UNPAID"}}`

### 4. Pay

```bash
curl -s -X POST https://www.vigilath.com/api/agent/pay \
  -H "Authorization: Bearer $VIGILATH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"orderNumber": "ORDER_NUMBER", "method": "points"}'
```

Methods:
- `points` — instant settlement, fully automated
- `stripe` — returns `paymentUrl`, show to user to complete card payment
- `coinbase` — returns `paymentUrl`, show to user to complete crypto payment

After stripe/coinbase, poll order status to confirm payment.

### 5. Query Orders

List orders:
```bash
curl -s https://www.vigilath.com/api/agent/orders \
  -H "Authorization: Bearer $VIGILATH_TOKEN"
```
Optional query params: `status` (1=pending_payment, 2=pending_shipment, 3=shipped, 5=completed, 6=cancelled), `page`, `page_size`.

Single order detail:
```bash
curl -s https://www.vigilath.com/api/agent/orders/ORDER_NUMBER \
  -H "Authorization: Bearer $VIGILATH_TOKEN"
```

### 6. Addresses

List addresses:
```bash
curl -s https://www.vigilath.com/api/agent/addresses \
  -H "Authorization: Bearer $VIGILATH_TOKEN"
```

Create address:
```bash
curl -s -X POST https://www.vigilath.com/api/agent/addresses \
  -H "Authorization: Bearer $VIGILATH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"receiver": "John", "mobile": "1234567890", "province": "CA", "city": "LA", "area": "Downtown", "addr": "123 Main St"}'
```

## Common Workflows

### Quick buy (no bargain)
1. Search: `POST /api/agent/shopping` with query
2. Show products to user, let them pick
3. Order: `POST /api/agent/order` with selected spuId(s)
4. Pay: `POST /api/agent/pay` with orderNumber

### Quick buy (autonomous — one call)
1. `POST /api/agent/shopping` with `autonomous: true` — AI picks and orders automatically
2. Pay: `POST /api/agent/pay` with orderNumber from response

### Bargain then buy
1. Search: `POST /api/agent/shopping` with `bargain: true`
2. For each bargain session, negotiate: `POST /api/agent/bargain` with counter-offers
3. On deal: `POST /api/agent/order` with `quoteId` from quote
4. Pay: `POST /api/agent/pay`

## Error Handling

- 401: Token expired or invalid — re-authenticate via Device Flow
- 404: Resource not found (order, session, address)
- 422: Validation error — check request body
- 429: Rate limited — wait and retry

## Discovery

For machine-readable capability metadata:
- `GET /.well-known/agent.json` — structured service discovery
- `GET /llms.txt` — LLM-readable summary
- `GET /llms-full.txt` — full API documentation
