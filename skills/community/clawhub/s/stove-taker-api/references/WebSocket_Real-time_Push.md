# WebSocket Real-time Push [â](#websocket-real-time-push)

## Connection Information [â](#connection-information)

**Connection Endpoint**: `wss://{host}/ws/taker/v1?types=order_status_change,cancellation_request`

**Description**: Provides real-time order status change and cancellation request push notifications for Takers. When order status changes or cancellation requests are received, the system automatically pushes notifications to relevant Takers.

**Authentication**: API Key credential authentication

## Query Parameters [â](#query-parameters)

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| types | string | Yes | URL query parameter for subscribing to specified message types, multiple types separated by commas. See `WebSocketDataType` enum type description |

## Order Status Change Notification [â](#order-status-change-notification)

When order status changes, you will receive messages in the following format:

```json
{
  "type": "order_status_change",
  "timestamp": "2024-01-01T12:00:00Z",
  "data": {
    "order_hash": "0x1234567890abcdef...",
    "maker": "0x1111111111111111111111111111111111111111",
    "taker": "0xabcdef1234567890...",
    "from_status": "pending",
    "to_status": "locked",
    "metadata": {
      "expires_at": "2024-01-01T13:00:00Z",
      "lock_id": "uuid-string",
      "blockchain_tx_hash": "0x..."
    }
  }
}
```

### Message Field Description [â](#message-field-description)

| Field | Type | Description |
| --- | --- | --- |
| type | string | Message type |
| timestamp | string | Timestamp |
| data | object | Order status change data |
| data.order_hash | string | Order hash |
| data.maker | string | Maker address |
| data.taker | string | Taker address |
| data.from_status | enum | Original status (see OrderStatus enum, may be null) |
| data.to_status | enum | New status (see OrderStatus enum) |
| data.metadata | object | Additional information (optional) |

## Order Cancellation Request Notification [â](#order-cancellation-request-notification)

When receiving order cancellation requests, you will receive messages in the following format:

```json
{
  "type": "cancellation_request",
  "timestamp": "2024-01-01T12:00:00Z",
  "data": {
    "order_hash": "0x1234567890abcdef...",
    "maker": "0x1111111111111111111111111111111111111111",
    "reason": "user_requested",
    "metadata": {
      "request_id": "uuid-string",
      "expires_at": "2024-01-01T13:00:00Z"
    }
  }
}
```

### Message Field Description [â](#message-field-description-1)

| Field | Type | Description |
| --- | --- | --- |
| type | string | Message type |
| timestamp | string | Timestamp |
| data | object | Cancellation request data |
| data.order_hash | string | Order hash |
| data.maker | string | Maker address |
| data.reason | string | Cancellation reason |
| data.metadata | object | Additional metadata |

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

## Authentication Method [â](#authentication-method)

Taker WebSocket connection uses API Key authentication, need to include valid API Key in request header:

Authorization: Bearer <your-api-key>

For browser environments, since WebSocket doesn't support custom request headers, you can pass API Key as query parameter:

```javascript
const ws = new WebSocket(
  `wss://${host}/ws/taker/v1?types=order_status_change,cancellation_request&api_key=<your-api-key>`
);

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  
  if (message.type === 'order_status_change') {
    console.log('Order status changed:', message.data);
  } else if (message.type === 'cancellation_request') {
    console.log('Cancellation request received:', message.data);
  } else if (message.type === 'heartbeat') {
    console.log('Heartbeat:', message.timestamp);
  }
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('WebSocket connection closed');
};
```

## Server Heartbeat [â](#server-heartbeat)

The server sends heartbeat messages to the connection at regular intervals in the following format:

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
| heartbeat | Server-side heartbeat notification. No need to specify in parameters |
| order_status_change | Order status change |
| cancellation_request | Order cancellation request |

## Notes [â](#notes)

- Recommend implementing automatic reconnection mechanism
- Handle heartbeat messages to keep connection alive
- Handle cancellation requests properly and respond promptly
- Pay attention to message sequencing, process by timestamp order
