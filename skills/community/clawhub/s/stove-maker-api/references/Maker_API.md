# Maker API [â](#maker-api)

## API Introduction [â](#api-introduction)

Maker API interfaces are provided for authenticated institutional clients (Web3 users), supporting order creation, position management, order status queries, and more. Access the platform via JWT authentication to place orders and initiate trades.

## Quick Start [â](#quick-start)

### Basic Information [â](#basic-information)

- **Test Environment**: `https://api-qa.proto.stove.finance`
- **Production Environment**: `https://proto.stove.finance`
- **Content-Type**: `application/json`
- **Data Format**: JSON (snake_case naming convention)
- **Authentication**: JWT Token

**Note**: API examples show relative paths (e.g., `/api/v1/orders`). Prepend the environment URL when making actual requests.

**Testing Guide**: For testing environment, please refer to [Testing Guide](./testing-guide.html) for order quantity rules and test scenarios.

### Unified Response Format [â](#unified-response-format)

All interfaces follow a unified response structure:

| Field | Type | Description |
| --- | --- | --- |
| code | int | Result code, 0 indicates success, non-0 indicates error |
| message | string | Error message (returned only on error) |
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

---

## API Overview [â](#api-overview)

### Account APIs [â](#account-apis)

- **Authorization** - Wallet connection and JWT token acquisition
- **Profile** - Get account profile information

### Order APIs [â](#order-apis)

- **Create Order** - Create new buy or sell orders
- **Cancel Order** - Cancel unfilled orders
- **Query Orders** - Query order list with various filters
- **Query Nonce** - Get next available order nonce value
- **Estimate Fee** - Estimate order fees
- **Query Positions** - Query held stock token information

### WebSocket [â](#websocket)

- **Real-time Push** - Subscribe to real-time order status change notifications

Please refer to the left navigation menu for detailed documentation of each API.

---

## Enum Type Descriptions [â](#enum-type-descriptions)

### OrderStatus - Order Status [â](#orderstatus-order-status)

| Enum | Description | Final State | Details |
| --- | --- | --- | --- |
| pending | Pending | No | Order created, waiting for Taker to lock. For example, orders waiting for US market opening remain in this state |
| locked | Locked | No | Order locked by Taker, may be in trading process |
| partially_filled | Partially filled | Yes | Order partially filled, remaining portion refunded. Usually occurs when user requests cancellation during execution, resulting in partial fill |
| filled | Fully filled | Yes | Order fully filled |
| cancelled | Cancelled | Yes | Order cancelled by Maker |
| expired | Expired | Yes | Order exceeded validity period |
| rejected | Rejected | Yes | Order validation failed or rejected by Taker, rejection reason typically provided |
| suspended | Suspended | No | Order suspended, requires manual intervention |

**Final State Note**: States marked as final (Yes) cannot transition to other states.

### Exchange - Exchange Code [â](#exchange-exchange-code)

| Index | Description |
| --- | --- |
| 0 | NASDAQ (US Stock Exchange) |

### Market - Market Code [â](#market-market-code)

| Enum | Description |
| --- | --- |
| usex | US Stock Market |

### MakerStatus - User Status [â](#makerstatus-user-status)

| Index | Description |
| --- | --- |
| 1 | Active |
| 2 | Inactive |
| 3 | Suspended |

## Notes [â](#notes)

- **Data Format**: All interfaces use snake_case naming convention
- **Amount Precision**: Amount fields use string type to avoid precision loss
- **Address Format**: Ethereum addresses must include `0x` prefix
- **Time Format**: Defaults to `ISO 8601 standard format`, e.g., `2025-11-17T03:00:24Z`
