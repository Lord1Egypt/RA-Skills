---
name: telnyx-cli
description: Telnyx API integration via CLI. Send SMS/MMS/WhatsApp messages, manage phone numbers, query call logs, debug webhooks, and access your Telnyx account. Use when interacting with Telnyx APIs, managing messaging, or accessing account data.
metadata: {"openclaw":{"emoji":"🔧","requires":{"bins":["telnyx"],"env":["TELNYX_API_KEY"]},"primaryEnv":"TELNYX_API_KEY"}}
---

# Telnyx CLI

Telnyx API integration for OpenClaw: messaging, phone numbers, webhooks, and account management.

## Setup

### 1. Install CLI

```bash
npm install -g @telnyx/api-cli
```

### 2. Configure API Key

```bash
telnyx auth setup
```

Paste your API key from: https://portal.telnyx.com/#/app/api-keys

Saves to `~/.config/telnyx/config.json` (persistent).

### 3. Verify

```bash
telnyx number list
```

## Commands

| Category | Command | Description |
|----------|---------|-------------|
| **Messaging** | `telnyx message send` | Send SMS/email/WhatsApp |
| | `telnyx message list` | List messages |
| | `telnyx message get` | Get message status |
| **Phone Numbers** | `telnyx number list` | Your phone numbers |
| | `telnyx number search` | Search available numbers |
| | `telnyx number buy` | Purchase a number |
| | `telnyx number release` | Release a number |
| **Calls** | `telnyx call list` | View calls |
| | `telnyx call get` | Get call details |
| **Webhooks** | `telnyx webhook list` | List webhooks |
| | `telnyx debugger list` | View webhook events |
| | `telnyx debugger retry` | Retry failed webhooks |
| **Account** | `telnyx account get` | Account info & balance |

## Usage

### Messaging

```bash
# Send SMS
telnyx message send --from +15551234567 --to +15559876543 --text "Hello!"

# List messages
telnyx message list

# Get status
telnyx message get MESSAGE_ID
```

### Phone Numbers

```bash
# List
telnyx number list

# Search
telnyx number search --country US --npa 415

# Buy
telnyx number buy --number "+15551234567"

# Release
telnyx number release "+15551234567"
```

### Webhooks & Debugging

```bash
# List webhooks
telnyx webhook list

# View failed deliveries
telnyx debugger list --status failed

# Retry failed
telnyx debugger retry EVENT_ID
```

### Account

```bash
# Account info
telnyx account get

# Check balance
telnyx account get --output json | jq '.balance'
```

## Output Formats

```bash
# Table (default)
telnyx number list

# JSON
telnyx number list --output json

# CSV
telnyx number list --output csv
```

## Examples

### Bulk Messaging

```bash
#!/bin/bash
while read phone; do
  telnyx message send --from +15551234567 --to "$phone" --text "Hello!"
  sleep 1  # Rate limiting
done < recipients.txt
```

### Monitor Webhooks

```bash
#!/bin/bash
while true; do
  FAILED=$(telnyx debugger list --status failed --output json | jq '.data | length')
  [ "$FAILED" -gt 0 ] && echo "⚠️  $FAILED failed webhooks"
  sleep 300
done
```

### Export Data

```bash
# CSV export
telnyx call list --limit 1000 --output csv > calls.csv

# JSON export
telnyx number list --output json > numbers.json
```

## Tips

- Rate limit: 100 req/s — add `sleep 1` for bulk operations
- Use `--output json` or `--output csv` to change format
- Get help: `telnyx COMMAND --help` (e.g., `telnyx message --help`)
- API Key location: `~/.config/telnyx/config.json`

## Integration with OpenClaw

```bash
# In cron jobs
0 9 * * * telnyx call list --limit 10 > /tmp/daily-calls.txt

# In heartbeat
telnyx debugger list --status failed

# In scripts
BALANCE=$(telnyx account get --output json | jq '.balance')
echo "Balance: $BALANCE"
```

## Troubleshooting

### CLI not found
```bash
npm install -g @telnyx/api-cli
```

### API key not configured
```bash
# Reconfigure
telnyx auth setup

# Or check existing config
cat ~/.config/telnyx/config.json
```

### Connection issues
```bash
# Test connection
telnyx account get
```

## Resources

- Telnyx Docs: https://developers.telnyx.com
- API Portal: https://portal.telnyx.com
- Telnyx CLI: https://github.com/team-telnyx/telnyx-api-cli
