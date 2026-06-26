# WebSocket (Compact)

Endpoints:
- Public: `wss://ws-contract.weex.com/v2/ws/public`
- Private: `wss://ws-contract.weex.com/v2/ws/private`

Control messages:

```json
{"event":"subscribe","channel":"channel_name"}
```

```json
{"event":"unsubscribe","channel":"channel_name"}
```

Heartbeat:
- reply pong for server ping

Private WS auth:
- docs specify header auth with `ACCESS-KEY`, `ACCESS-PASSPHRASE`, `ACCESS-TIMESTAMP`, `ACCESS-SIGN`
- private WS signing message: `timestamp + /v2/ws/private`

Reference:
- https://www.weex.com/api-doc/contract/Websocket/websocket-intro
