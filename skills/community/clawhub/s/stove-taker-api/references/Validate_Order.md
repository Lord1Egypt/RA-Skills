# Validate Order [â](#validate-order)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `POST /api/v1/orders/validate`

**Description**: Validate order validity (does not create order)

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

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| valid | boolean | Whether order is valid |
| order_hash | string | Order hash |
| errors | array | Error list |
| maker_balance | string | Maker balance |
| maker_allowance | string | Maker allowance |
| nonce_valid | boolean | Whether nonce is valid |
| signature_valid | boolean | Whether signature is valid |
| not_expired | boolean | Whether not expired |

## Request Example [â](#request-example)

```bash
curl -X POST "/api/v1/orders/validate" \
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
       "signature": "0x..."
     }'
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": {
        "valid": true,
        "order_hash": "0x1234567890abcdef...",
        "errors": [],
        "maker_balance": "10000000000000000000000",
        "maker_allowance": "5000000000000000000000",
        "nonce_valid": true,
        "signature_valid": true,
        "not_expired": true
    }
}
```

## Notes [â](#notes)

- This endpoint only validates orders, does not create them
- Can be used for pre-checks before locking orders
- Validation includes: balance, allowance, nonce, signature, expiration time, etc.
