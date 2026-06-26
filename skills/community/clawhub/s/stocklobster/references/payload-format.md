# StockLobster Payload Format

## Confirmed simple payload

The currently confirmed working payload sent to OpenClaw is:

```json
{
  "text": "StockLobster alert\nSymbol: TEST\nEvent: screen_hit\nMessage: TEST hit momentum criteria\nPrice: 4.92\nChange: 3.4%\nVolume: 1234567\nStrategy: momentum\nTimestamp: 2026-04-08T02:21:00.000Z"
}
```

For the simple ingestion path, the OpenClaw mapping should reference:

```text
{{payload.text}}
```

## Earlier structured payload shape

An earlier StockLobster payload shape discussed during setup used these fields:

```json
{
  "source": "stocklobster",
  "event": "screen_hit",
  "symbol": "TEST",
  "message": "TEST hit momentum criteria",
  "timestamp": "2026-04-08T02:21:00.000Z",
  "data": {
    "price": 4.92,
    "changePct": 3.4,
    "volume": 1234567,
    "strategy": "momentum"
  }
}
```

If you return to this structured format later, map fields with `payload`, for example:

```text
{{payload.symbol}}
{{payload.event}}
{{payload.message}}
{{payload.data.price}}
{{payload.data.changePct}}
{{payload.data.volume}}
{{payload.data.strategy}}
{{payload.timestamp}}
```

## Template rule that matters

In this OpenClaw build, hook templates resolve against the request body as `payload`, not `json`.

Use:
- `{{payload.text}}`
- `{{payload.symbol}}`
- `{{payload.data.price}}`

Do not use:
- `{{json.text}}`
- `{{json.symbol}}`
