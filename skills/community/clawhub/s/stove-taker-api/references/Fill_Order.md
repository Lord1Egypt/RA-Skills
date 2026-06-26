# Fill Order [â](#fill-order)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `POST /api/v1/orders/fill`

**Description**: Execute order fill (partial or full). This endpoint requires Taker authentication.

**Authentication**: API Key credential authentication

## Request Parameters [â](#request-parameters)

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| order | object | Yes | Order information |
| order.maker | string | Yes | Order creator address |
| order.principal | string | Yes | Recipient address |
| order.is_buy | bool | Yes | Whether it's a buy order |
| order.ticker | string | Yes | Stock symbol |
| order.exchange | int | Yes | Exchange ID |
| order.asset | string | Yes | Asset token address |
| order.price | string | Yes | Price |
| order.quantity | string | Yes | Quantity |
| order.incentive | string | Yes | Incentive amount |
| order.deadline | long | Yes | Deadline timestamp |
| order.nonce | long | Yes | Anti-replay nonce |
| signature | string | Yes | Order signature |
| fill_quantity | string | Yes | Fill quantity |
| taker_incentive | string | Yes | Actual transaction fee |

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| success | boolean | Whether fill succeeded |
| tx_hash | string | Transaction hash |
| order_hash | string | Order hash |
| filled_quantity | string | Filled quantity |
| filled_amount | string | Filled amount |
| fee_amount | string | Fee amount |
| incentive_amount | string | Incentive amount |
| status | enum | Order status (see OrderStatus) |

## Request Example [â](#request-example)

```bash
curl -X POST "/api/v1/orders/fill" \
     -H "X-API-Key: YOUR_API_KEY" \
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
       "signature": "0x...",
       "fill_quantity": "50",
       "taker_incentive": "500000000000000000"
     }'
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": {
        "success": true,
        "tx_hash": "0xabcdef1234567890...",
        "order_hash": "0x1234567890abcdef...",
        "filled_quantity": "50",
        "filled_amount": "7512500000000000000000",
        "fee_amount": "75125000000000000000",
        "incentive_amount": "500000000000000000",
        "status": "partially_filled"
    }
}
```

## Enum Types [â](#enum-types)

### OrderStatus - Order Status [â](#orderstatus-order-status)

| Enum | Description |
| --- | --- |
| partially_filled | Partially filled |
| filled | Fully filled |

## Notes [â](#notes)

- Fill quantity cannot exceed remaining order quantity
- Order must be in locked status to be filled
- After partial fill, order status becomes partially_filled
- After complete fill, order status becomes filled
