# Public API [â](#public-api)

## API Introduction [â](#api-introduction)

Public API interfaces are open to all users and can be accessed without authentication. These interfaces provide platform statistics, orderbook information, and ticker statistics, offering transparent market data access for all users.

## Basic Information [â](#basic-information)

- **Test Environment**: `https://api-qa.proto.stove.finance`
- **Production Environment**: `https://proto.stove.finance`
- **Content-Type**: `application/json`
- **Data Format**: JSON (snake_case naming convention)

**Note**: API examples show relative paths (e.g., `/api/v1/orders`). Prepend the environment URL when making actual requests.

## Unified Response Format [â](#unified-response-format)

All interfaces follow a unified response structure:

| Field | Type | Description |
| --- | --- | --- |
| code | int | Result code, 0 indicates success, non-0 indicates error |
| message | string | Error message, brief description (returned only on error) |
| details | string | Additional error information (returned only on error) |
| data | object | Business data (returned only on success) |

**Success Response Example**:

```json
{
	"code": 0,
	"data": {
		// Specific business data
	}
}
```

**Error Response Example**:

```json
{
	"code": 400001,
	"message": "Invalid parameter",
	"details": "The wallet_address field is required"
}
```

---

## API Overview [â](#api-overview)

Public API provides the following main features:

- **Platform Statistics** - Query platform user count, order count, and stock token count
- **Orderbook** - Query buy and sell order information for specific stocks
- **Ticker Statistics** - Query basic information and trading statistics for stocks
- **Ticker Heatmap** - Query heatmap data for popular market stocks

Please click the left navigation bar to view detailed documentation for each interface.

---

## Enum Type Descriptions [â](#enum-type-descriptions)

### Exchange - Exchange Code [â](#exchange-exchange-code)

| Index | Description |
| --- | --- |
| 0 | NASDAQ (US Stock Exchange) |

### Market - Market Code [â](#market-market-code)

| Enum | Description |
| --- | --- |
| usex | US Stock Market |

## Notes [â](#notes)

- **Data Format**: All interfaces use snake_case naming convention
- **Amount Precision**: Amount fields use string type to avoid precision loss
- **Address Format**: Ethereum addresses must include `0x` prefix
- **Time Format**: Unless otherwise specified, time format defaults to `ISO 8601 standard format`, e.g., `2025-11-17T03:00:24Z`
