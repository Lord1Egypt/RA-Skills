# Estimate Order Fee [â](#estimate-order-fee)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `POST /api/v1/orders/estimate_charge`

**Description**: Estimate order fee with automatic exchange rate conversion

**Authentication**: `Authorization` header with JWT token

## Request Parameters [â](#request-parameters)

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| is_buy | bool | Yes | Whether it's a buy order |
| ticker | string | Yes | Stock symbol |
| exchange | int | Yes | Exchange code (0=US Stock) |
| quantity | string | Yes | Quantity (regular precision) |
| price | string | Yes | **Stock's native currency price (regular precision, NOT wei)**USD for US stocks |
| asset | string | Yes | USDT contract address |
| target_currency | string | No | Target stablecoin (USDT or USDC), defaults to USDT |

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| base_currency | string | Base currency (USD for US stocks) |
| charge_base | string | Fee in base currency (regular precision) |
| target_currency | string | Target stablecoin (USDT or USDC) |
| charge_target | string | Fee in target stablecoin (wei precision, 18 decimals) |
| price_base | string | Price in base currency (regular precision, same as request price) |
| price_target | string | Price in target currency (wei precision, 18 decimals) |
| exchange_rate | float | Exchange rate from base currency to target currency |

## Request Example [â](#request-example)

```bash
curl -X POST "/api/v1/orders/estimate_charge" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     -H "Content-Type: application/json" \
     -d '{
       "is_buy": true,
       "ticker": "AAPL",
       "exchange": 0,
       "quantity": "100",
       "price": "260",
       "asset": "0x09671802Cc9Bbf6402f2e7a07b220Aa7b43D8c91"
     }'
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": {
        "base_currency": "USD",
        "charge_base": "3.36",
        "target_currency": "USDT",
        "charge_target": "3377745527638190000",
        "price_base": "260",
        "price_target": "261373165829145650000",
        "exchange_rate": 0.994746339683381
    }
}
```

## Notes [â](#notes)

- **Input Parameter Precision**: `quantity` uses regular precision (e.g., "100" means 100 shares)`price` uses regular precision (e.g., "260" means $260/share), **Note: This is the stock's native currency price, NOT wei precision**
- **Output Parameter Precision**: `charge_base` uses regular precision`charge_target` uses wei precision (18 decimals)`price_target` uses wei precision (18 decimals)
- Automatic currency conversion from stock's native currency (USD) to target stablecoin
- Supports target_currency parameter to specify output stablecoin (USDT or USDC), defaults to USDT
- Fee estimate is for reference only, actual fee is determined at transaction time
