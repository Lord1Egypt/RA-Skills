# Taker API [â](#taker-api)

## API Introduction [â](#api-introduction)

Taker API interfaces are provided for authenticated brokers or stock custodian institutions, supporting order locking, order filling, transaction record queries, and more. Access the platform via API Key authentication to complete off-chain stock order transactions.

## Quick Start [â](#quick-start)

### Basic Information [â](#basic-information)

- **Test Environment**: `https://api-qa.proto.stove.finance`
- **Production Environment**: `https://proto.stove.finance`
- **Content-Type**: `application/json`
- **Data Format**: JSON (snake_case naming convention)
- **Authentication**: API Key

**Note**: API examples show relative paths (e.g., `/api/v1/orders`). Prepend the environment URL when making actual requests.

### Unified Response Format [â](#unified-response-format)

All interfaces follow a unified response structure:

| Field | Type | Description |
| --- | --- | --- |
| code | int | Result code, 0 indicates success, non-0 indicates error |
| message | string | Error message (returned only on error) |
| details | string | Additional error information (returned only on error) |
| data | object | Business data (returned only on success) |

---

## API Overview [â](#api-overview)

### Account Endpoints [â](#account-endpoints)

- **Account Connection** - Perform wallet connection to obtain JWT token

### Order Endpoints [â](#order-endpoints)

- **Validate Order** - Validate order validity (does not create order)
- **Lock Order** - Lock order for filling
- **Unlock Order** - Unlock locked order
- **Fill Order** - Execute order fill (partial or full)
- **Reject Order** - Reject order
- **Query Orders** - Query orders locked or filled by taker
- **Fill Records** - Query order fill records

### WebSocket [â](#websocket)

- **Real-time Push** - Subscribe to real-time notifications of order status changes and cancellation requests

Please click the left navigation bar to view detailed documentation for each interface.

---

## Enum Type Descriptions [â](#enum-type-descriptions)

### OrderStatus - Order Status [â](#orderstatus-order-status)

| Enum | Description | Is Final | Details |
| --- | --- | --- | --- |
| pending | Pending | No | Order created, waiting for Taker to lock. For example, also in this state when waiting for US market to open |
| locked | Locked | No | Order locked by Taker, may be in trading |
| partially_filled | Partially filled | Yes | Order partially filled, remaining portion refunded. Usually occurs when user requests cancellation during filling process, resulting in partial fill |
| filled | Fully filled | Yes | Order fully filled |
| cancelled | Cancelled | Yes | Order cancelled by Maker |
| expired | Expired | Yes | Order exceeded validity period |
| rejected | Rejected | Yes | Order validation failed or rejected by Taker, usually with rejection reason provided |
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

## Notes [â](#notes)

- **Data Format**: All interfaces use snake_case naming convention
- **Amount Precision**: Amount fields use string type to avoid precision loss
- **Address Format**: Ethereum addresses must include `0x` prefix
- **Time Format**: Defaults to `ISO 8601 standard format`, e.g., `2025-11-17T03:00:24Z`
