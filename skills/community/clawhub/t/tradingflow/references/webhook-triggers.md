# Webhooks & Triggers

TradingFlow supports event-driven automation through webhooks and trigger configurations.

## Webhooks

Webhooks connect external services to your TFP processes. Each webhook is linked to a specific process.

### Creating a Webhook

```bash
curl -X POST $BASE/webhook \
  -H "Authorization: Bearer $KEY" \
  -d '{
    "processId": "abc123",
    "name": "price-alert",
    "type": "inbound",
    "events": ["trigger"],
    "secret": "optional_hmac_secret"
  }'
```

Response:

```json
{
  "data": {
    "_id": "wh_abc123",
    "name": "price-alert",
    "type": "inbound",
    "inboundUrl": "https://api.tradingflow.fun/api/v1/webhook/inbound/tok_xyz789",
    "events": ["trigger"],
    "isActive": true
  }
}
```

### Triggering a Webhook

External services send POST requests to the `inboundUrl`. No authentication required.

```bash
curl -X POST https://api.tradingflow.fun/api/v1/webhook/inbound/tok_xyz789 \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTCUSDT", "price": 42000, "signal": "buy"}'
```

The payload is forwarded to the linked TFP process.

### Managing Webhooks

```bash
# List webhooks for a process
curl "$BASE/webhook/list/{processId}" \
  -H "Authorization: Bearer $KEY"

# Get webhook details
curl "$BASE/webhook/{id}" \
  -H "Authorization: Bearer $KEY"

# Delete webhook
curl -X DELETE "$BASE/webhook/{id}" \
  -H "Authorization: Bearer $KEY"
```

### Webhook Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| processId | string | yes | Target TFP process ID |
| name | string | yes | Display name |
| type | string | yes | Webhook type (e.g. `inbound`) |
| events | string[] | yes | Event names to listen for |
| targetUrl | string | no | Outbound: URL to call |
| headers | object | no | Outbound: custom headers |
| secret | string | no | HMAC secret for signature verification |

## Trigger Types

Triggers are defined at the strategy level and determine when a process executes.

### Cron Trigger

Periodic execution using cron expressions.

```json
{
  "type": "cron",
  "config": {
    "schedule": "0 9 * * 1"
  }
}
```

Common schedules:
| Expression | Description |
|------------|-------------|
| `* * * * *` | Every minute |
| `*/5 * * * *` | Every 5 minutes |
| `0 * * * *` | Every hour |
| `0 9 * * *` | Daily at 9:00 UTC |
| `0 9 * * 1` | Every Monday at 9:00 UTC |
| `0 0 1 * *` | First of each month |

### Webhook Trigger

Triggered by incoming webhook calls.

```json
{
  "type": "webhook",
  "config": {
    "events": ["trigger", "price_update"]
  }
}
```

### Price Alert Trigger

Triggered when a token price meets a condition.

```json
{
  "type": "price_alert",
  "config": {
    "token": "BTC",
    "condition": "below",
    "threshold": 40000
  }
}
```

Conditions: `above`, `below`, `crosses_above`, `crosses_below`

### Manual Trigger

No automatic execution. Process runs only when explicitly started.

```json
{
  "type": "manual",
  "config": {}
}
```

## Combining Triggers with Operators

A strategy can use triggers for timing and operators for execution:

```
TRIGGERS:
- type: cron
  config:
    schedule: "*/15 * * * *"

OPERATORS:
- vault-bsc
- logging
- notify
```

This configuration runs every 15 minutes and has access to BSC vault operations, logging, and notifications.

## Use Cases

### TradingView Alert → Auto Trade

1. Create a webhook linked to your TFP process
2. Configure TradingView to send alerts to the `inboundUrl`
3. Your process receives the alert payload and executes the trade

```python
# In your TFP process (main.py)
import json
import sys

# Webhook payload arrives via stdin or env
payload = json.loads(sys.stdin.read())
signal = payload.get("signal")  # "buy" or "sell"

if signal == "buy":
    # Use vault operator to swap USDT → BTC
    pass
```

### Price Monitor → Notification

1. Set up a cron trigger (every 5 minutes)
2. Process fetches prices and checks conditions
3. If condition met, send notification via `notify` operator

### Multi-Signal Strategy

1. Multiple webhooks feed signals (TradingView, on-chain events, social sentiment)
2. Process aggregates signals and makes decisions
3. Executes via vault operator when confidence threshold met
