# Order Status Event Push [â](#order-status-event-push)

## Connection Information [â](#connection-information)

**Connection Endpoint**: `wss://{host}/ws/maker/v1?types=order_status_change`

**Description**: Provides real-time order status change push notifications for Makers. When order status changes, the system automatically pushes notifications to relevant Makers.

**Authentication**: `Authorization` header with JWT token

## Query Parameters [â](#query-parameters)

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| types | string | Yes | URL query parameter for subscribing to specified message types, multiple types separated by commas. See `WebSocketDataType` enum type description for details |

## Order Status Change Notification [â](#order-status-change-notification)

When order status changes, you will receive messages in the following format:

```json
{
  "type": "order_status_change",
  "timestamp": "2024-01-01T12:00:00Z",
  "data": {
    "order_hash": "0x1234567890abcdef...",
    "maker": "0x1111111111111111111111111111111111111111",
    "from_status": "pending",
    "to_status": "locked",
    "metadata": {
      "taker_address": "0xabcdef1234567890...",
      "expires_at": "2024-01-01T13:00:00Z",
      "lock_id": "uuid-string"
    }
  }
}
```

## Message Field Description [â](#message-field-description)

| Field | Type | Description |
| --- | --- | --- |
| type | string | Message type |
| timestamp | string | Timestamp |
| data | object | Order status change data |
| data.order_hash | string | Order hash |
| data.maker | string | Maker address |
| data.from_status | enum | Original status (may be null) |
| data.to_status | enum | New status |
| data.metadata | object | Additional information (optional) |

## Status Change Trigger Scenarios [â](#status-change-trigger-scenarios)

### 1. Order Creation [â](#_1-order-creation)

- `null` â `pending`: Order created successfully
- `null` â `rejected`: Order validation failed

### 2. Taker Operations [â](#_2-taker-operations)

- `pending` â `locked`: Taker locks order
- `locked` â `pending`: Taker unlocks order
- `locked` â `rejected`: Taker rejects order
- `pending/locked` â `partially_filled`: Order partially filled
- `partially_filled` â `filled`: Order fully filled

### 3. Maker Operations [â](#_3-maker-operations)

- `pending` â `cancelled`: Maker cancels order

### 4. System Operations [â](#_4-system-operations)

- `pending` â `expired`: Order automatically expires
- Any status â `suspended`: System exception, requires manual intervention

## Browser Support [â](#browser-support)

Due to browser WebSocket security policies, `Authorization` header is not supported, but can be passed through subprotocols:

```javascript
const ws = new WebSocket(
  `wss://${host}/ws/maker/v1?types=order_status_change`, 
  ['jwt', jwt]
);

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Received:', message);
};
```

## Server Heartbeat [â](#server-heartbeat)

The server sends heartbeat messages to the connection at regular intervals:

```json
{
  "type": "heartbeat",
  "timestamp": 1763722070521
}
```

## Enum Types [â](#enum-types)

### WebSocketDataType - WebSocket Message Type [â](#websocketdatatype-websocket-message-type)

| Enum | Description |
| --- | --- |
| heartbeat | Server-side heartbeat notification |
| order_status_change | Order status change |
