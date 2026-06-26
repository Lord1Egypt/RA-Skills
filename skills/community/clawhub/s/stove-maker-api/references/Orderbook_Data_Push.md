# Orderbook Data Push [â](#orderbook-data-push)

## Connection Information [â](#connection-information)

**Connection Endpoint**: `wss://{host}/ws/orderbooks/v1?symbols=doge@dcex/eth@dcex`

**Description**: Provides real-time orderbook data push for Makers

**Authentication**: JWT token passed through subprotocols

## Query Parameters [â](#query-parameters)

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| symbols | string | Yes | URL parameter, single format is `{symbol}@{market}`, multiple separated by `/`. Market possible values are `usex`/`hkex`/`dcex`. US stock single format can omit market, i.e., no need for `@{market}` part |

## Orderbook Update Notification [â](#orderbook-update-notification)

When orderbook data updates, you will receive messages in the following format:

```json
{
  "type": "orderbook_update",
  "timestamp": "2026-01-19T06:55:49.301529733Z",
  "data": {
    "symbol": "DOGE",
    "market": "dcex",
    "bid": [],
    "ask": [
      {
        "price": 0.12988,
        "volume": 6.0
      },
      {
        "price": 0.13083,
        "volume": 5.0
      }
    ],
    "time": "2025-12-24T01:33:24Z"
  }
}
```

## Message Field Description [â](#message-field-description)

| Field | Type | Description |
| --- | --- | --- |
| type | string | Message type |
| timestamp | string | Timestamp, message time |
| data | object | Orderbook update data |
| data.symbol | string | Stock symbol |
| data.market | string | Market code enum. See `Market` enum type description for details |
| data.ask | object array | Ask orders |
| data.ask[].price | decimal | Price in corresponding market |
| data.ask[].volume | decimal | Volume |
| data.bid | object array | Bid orders |
| data.bid[].price | decimal | Price in corresponding market |
| data.bid[].volume | decimal | Volume |
| data.time | string | Data time |

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
