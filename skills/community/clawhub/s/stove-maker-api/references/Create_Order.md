# Create Order [â](#create-order)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `POST /api/v1/orders`

**Description**: Create a new order. Order creator must ensure sufficient balance and authorization

**Authentication**: `Authorization` header with JWT token

**Important**: Before creating an order, you need to sign the order data using the EIP-712 standard. See [Order Signature](./signature.html)

## Request Parameters [â](#request-parameters)

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| order | object | Yes | Order information |
| order.maker | string | Yes | Order creator address (must match the user address in JWT token) |
| order.principal | string | Yes | Recipient address |
| order.is_buy | bool | Yes | Whether it's a buy order |
| order.ticker | string | Yes | Stock symbol |
| order.exchange | int | Yes | Exchange code. See [`Exchange`](./../overview.html#exchange-exchange-code) enum type description |
| order.asset | string | Yes | Asset token address |
| order.price | string | Yes | Price (in wei, 18 decimals precision). Since the platform only accepts stablecoins, the order price needs to consider exchange rate conversion. It's recommended to use the [Estimate Order Fee](./estimate.html) API to get the exchange rate converted price |
| order.quantity | string | Yes | Quantity |
| order.incentive | string | Yes | Incentive amount (fee provided by Maker). This is the fee Maker offers for order execution. Only when `order.incentive >= estimated fee` will brokers lock and execute the order. Use [Estimate Order Fee](./estimate.html) API to get the estimated fee |
| order.deadline | long | Yes | Order signature validity deadline timestamp (Unix timestamp in seconds). Must be at least current time + 720 hours (30 days). For limit orders, it's recommended to set a longer validity period to ensure sufficient time for execution |
| order.nonce | long | Yes | Anti-replay nonce |
| signature | string | Yes | Order signature (signed using EIP-712 standard, see [Order Signature](./signature.html)) |

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| id | uuid | Order unique identifier |
| maker | string | Order creator address |
| principal | string | Recipient address |
| is_buy | bool | Whether it's a buy order |
| ticker | string | Stock symbol |
| exchange | int | Exchange code. See [`Exchange`](./../overview.html#exchange-exchange-code) enum type description |
| asset | string | Asset token address |
| price | string | Price |
| quantity | string | Quantity |
| incentive | string | Incentive amount |
| deadline | long | Deadline timestamp |
| nonce | long | Anti-replay nonce |
| signature | string | Order signature |
| order_hash | string | Order hash |
| status | enum | Order status. See [`OrderStatus`](./../overview.html#orderstatus-order-status) enum type description |
| filled_quantity | string | Filled quantity |
| created_at | string | Creation time |
| updated_at | string | Update time |

## Request Example [â](#request-example)

```bash
curl -X POST "/api/v1/orders" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     -H "Content-Type: application/json" \
     -d '{
       "order": {
         "maker": "0x1234567890123456789012345678901234567890",
         "principal": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
         "is_buy": true,
         "ticker": "AAPL",
         "exchange": 0,
         "asset": "0x0000000000000000000000000000000000000001",
         "price": "150250000000000000000",
         "quantity": "100",
         "incentive": "1000000000000000000",
         "deadline": 1735689600,
         "nonce": 1
       },
       "signature": "0x..."
     }'
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "maker": "0x1234567890123456789012345678901234567890",
        "principal": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
        "is_buy": true,
        "ticker": "AAPL",
        "exchange": 0,
        "asset": "0x0000000000000000000000000000000000000001",
        "price": "150250000000000000000",
        "quantity": "100",
        "incentive": "1000000000000000000",
        "deadline": 1735689600,
        "nonce": 1,
        "signature": "0x...",
        "order_hash": "0x1234567890abcdef...",
        "status": "pending",
        "filled_quantity": "0",
        "created_at": "2025-01-17T03:00:24Z",
        "updated_at": "2025-01-17T03:00:24Z"
    }
}
```
