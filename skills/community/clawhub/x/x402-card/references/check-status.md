# Check Card Status

## Command

```bash
# Single query
npx @aeon-ai-pay/x402-card status --order-no <orderNo>

# Poll until terminal status (SUCCESS or FAIL)
npx @aeon-ai-pay/x402-card status --order-no <orderNo> --poll
```

## Response Format

```json
{
  "code": "0",
  "msg": "success",
  "model": {
    "orderNo": "300217748668047431791",
    "orderStatus": "SUCCESS",
    "channelStatus": "COMPLETED",
    "orderAmount": 0.6,
    "txHash": "0xabc...def",
    "cardLastFour": "4321",
    "cardBin": "485932",
    "cardScheme": "VISA",
    "cardBalance": 0.6,
    "cardStatus": "ACTIVE"
  }
}
```

## Status Values

### orderStatus

| Status | Meaning | Action |
|--------|---------|--------|
| `INIT` | Order created, no payment yet | Wait |
| `PENDING` | Payment submitted, chain confirming | Poll again |
| `SUCCESS` | Card created | Show card details |
| `FAIL` | Failed | Show error, suggest retry |

### channelStatus

| Status | Meaning |
|--------|---------|
| `INIT` | Not sent to card provider |
| `PROCESSING` | Provider creating card |
| `COMPLETED` | Card ready |
| `FAILED` | Card creation failed |

### cardStatus

| Status | Meaning |
|--------|---------|
| `PENDING` | Provisioning |
| `ACTIVE` | Ready to use |
| `FROZEN` | Suspended |
| `CANCELLED` | Closed |

## Polling Behavior

With `--poll`:
- Polls every **5 seconds**, max **10 attempts** (50s total)
- Stops on `SUCCESS` or `FAIL`
- If timeout, inform user and provide manual check command
