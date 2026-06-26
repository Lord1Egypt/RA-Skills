# Global Reference

## ⚠️ Security Warning

**Before using this skill:**

- **Credentials are required**: DWS_CLIENT_ID and DWS_CLIENT_SECRET from DingTalk Open Platform
- **Enterprise admin approval** may be needed for whitelist access
- **Test in sandbox first** before production use
- **Use least-privilege credentials** with minimum required permissions

## Authentication

### First-Time Setup

```bash
# 1. Create app in DingTalk Open Platform
# https://open-dev.dingtalk.com/fe/app

# 2. Configure redirect URLs in app settings:
#    http://127.0.0.1 (local login)
#    https://login.dingtalk.com (device-flow for headless)

# 3. Login with credentials
dws auth login --client-id <app-key> --client-secret <app-secret>
```

### Environment Variables

```bash
export DWS_CLIENT_ID=<app-key>
export DWS_CLIENT_SECRET=<app-secret>
dws auth login
```

**Security note**: Environment variables may be exposed in logs. Prefer interactive login which stores credentials encrypted in system Keychain.

### Token Management

- Tokens are stored encrypted in system Keychain (macOS/Windows) or libsecret (Linux)
- Automatic refresh on expiry
- No manual intervention needed
- **Never share your credentials** or commit them to version control

## Output Formats

### JSON (Default)

All commands return JSON by default.

### Table Format

```bash
dws contact user search --keyword "test" -f table
```

### Raw Format

```bash
dws contact user get-self -f raw
```

### jq Filtering

```bash
# Extract specific fields
dws contact user search --keyword "test" --jq '.result[] | {name: .orgUserName, userId: .userId}'

# Count results
dws todo task list --jq '.result | length'

# Complex transformation
dws calendar event list --jq '.result[] | "\(.startTime): \(.title)"'
```

### Field Selection

```bash
# Return only specific fields
dws aitable record query --base-id <baseId> --table-id <tableId> --fields invocation,response
```

## Global Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--dry-run` | Preview without executing | `dws todo task create --dry-run` |
| `--yes` | Skip confirmations | `dws todo task create --yes` |
| `--jq <expr>` | Filter output with jq | `--jq '.result[]'` |
| `--fields <fields>` | Select specific fields | `--fields invocation,response` |
| `-f <format>` | Output format | `-f table`, `-f json`, `-f raw` |
| `--timeout <seconds>` | Request timeout | `--timeout 30` |

## Input Methods

### File Input

```bash
# Read from file
dws chat message send-by-bot --robot-code <code> --group <id> --text @message.md

# Read from stdin
cat message.md | dws chat message send-by-bot --robot-code <code> --group <id>
```

### JSON Input

```bash
# Inline JSON
dws aitable record create --base-id <base> --table-id <table> --fields '{"name": "Task 1"}'

# From file
dws aitable record create --base-id <base> --table-id <table> --fields @fields.json
```

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `INVALID_TOKEN` | Token expired | Run `dws auth login` |
| `PERMISSION_DENIED` | App lacks permission | Check app permissions in Open Platform |
| `RESOURCE_NOT_FOUND` | Invalid ID | Verify ID with schema introspection |
| `RATE_LIMITED` | Too many requests | Wait and retry |

### Recovery Event

When encountering `RECOVERY_EVENT_ID`:

```bash
dws --recovery <RECOVERY_EVENT_ID>
```

### Debug Mode

```bash
# Enable verbose logging
export DWS_DEBUG=1
dws contact user search --keyword "test"
```

## Schema Introspection

### Discover Capabilities

```bash
# List all products
dws schema --jq '.products[] | {id, tool_count: (.tools | length)}'

# Get product tools
dws schema --jq '.products[] | select(.id == "aitable") | .tools[] | .name'
```

### Inspect Tool Parameters

```bash
# Full schema
dws schema aitable.query_records

# Required fields only
dws schema aitable.query_records --jq '.tool.required'

# Parameter details
dws schema aitable.query_records --jq '.tool.parameters.properties'
```

## Auto-Correction Examples

`dws` automatically corrects common AI mistakes:

```bash
# camelCase → kebab-case
dws aitable record query --baseId BASE_ID
# Auto-corrected to: --base-id BASE_ID

# Sticky arguments
dws contact user search --keyword "test"--limit50
# Auto-corrected to: --keyword "test" --limit 50

# Fuzzy matching
dws aitable record query --tabel-id TABLE_ID
# Auto-corrected to: --table-id TABLE_ID

# Value normalization
dws todo task create --priority "1" --due-date "2024/03/29"
# Auto-corrected to: --priority 1 --due-date "2024-03-29"
```

## Best Practices

### For Agents

1. **Always use `--dry-run` first** for mutations
2. **Use `--yes`** to skip interactive prompts
3. **Use `--jq`** to reduce token consumption
4. **Discover with `dws schema`** before making calls

### Safe Execution Pattern

```bash
# 1. Preview
dws todo task create --title "Test" --executors "user123" --dry-run

# 2. Execute
dws todo task create --title "Test" --executors "user123" --yes
```

### Token Efficiency

```bash
# Bad: Returns full response
dws contact user search --keyword "test"

# Good: Extract only needed fields
dws contact user search --keyword "test" --jq '.result[] | {name: .orgUserName, userId: .userId}'
```
