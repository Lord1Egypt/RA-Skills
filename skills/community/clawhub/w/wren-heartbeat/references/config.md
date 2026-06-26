# Config Reference

## Full heartbeat.yaml Schema

```yaml
# Collectors — gather data from external sources
collectors:
  - name: string          # Required. Unique identifier.
    command: string        # Required. Shell command to run.
    format: text|json      # Output format. Default: text.
    alert: string          # Condition that triggers "action needed".
    summary: string        # Template for the summary line. Use {{output}}, {{.field}} for JSON.
    timeout: number        # Per-collector timeout in seconds. Default: from settings.timeout.
    cache: string          # Path to cache file for "changed" alert type.
    enabled: boolean       # Default: true. Set false to skip without removing.

# Health checks — monitor system state
health:
  - name: string          # Required. Unique identifier.
    command: string        # Required. Shell command to run (should output a number or string).
    warn: string           # Condition for warning level (yellow).
    critical: string       # Condition for critical level (red).
    alert: string          # Condition for action needed (alternative to warn/critical).
    summary: string        # Template for the summary line.
    enabled: boolean       # Default: true.

# Settings
settings:
  timeout: number         # Global timeout per check in seconds. Default: 30.
  parallel: boolean       # Run checks in parallel. Default: true.
  output: string          # Path to write summary. Default: research/latest.md.
  cache_dir: string       # Directory for "changed" caches. Default: .heartbeat-cache/
```

## Alert Conditions

### For text output:
- `!= ''` — alert if output is not empty
- `== 'string'` — alert if output equals string
- `!= 'string'` — alert if output does not equal string
- `contains 'string'` — alert if output contains string
- `> N` / `< N` / `>= N` / `<= N` — numeric comparison
- `changed` — alert if output differs from cached value (requires `cache` field)

### For JSON output:
- `.field > N` — compare JSON field to number
- `.field == 'string'` — compare JSON field to string
- `.field != null` — check JSON field exists
- `.count > 0` — common pattern for unread counts

### Summary Templates

Use `{{output}}` for full output or `{{.field}}` for JSON fields:
- `"{{.count}} unread emails"` → "3 unread emails"
- `"site returned {{output}}"` → "site returned 503"
- `"balance: {{.balance}} SOL"` → "balance: 1.5 SOL"

## Example Configs

### Minimal (just uptime)
```yaml
collectors:
  - name: site
    command: "curl -s -o /dev/null -w '%{http_code}' https://example.com"
    alert: "!= 200"
```

### Full agent setup
```yaml
collectors:
  - name: email
    command: "curl -s https://email-api.example.com/inbox -H 'X-API-Key: $EMAIL_KEY'"
    format: json
    alert: ".count > 0"
    summary: "{{.count}} new emails"

  - name: mentions
    command: "node tools/check-mentions.js"
    format: json
    alert: ".unread > 0"
    summary: "{{.unread}} unread mentions"

  - name: community
    command: "curl -s https://logger.example.com/messages?unread=true -H 'X-API-Key: $TG_KEY'"
    format: json
    alert: ".count > 0"
    summary: "{{.count}} new community messages"

  - name: market
    command: "node tools/check-price.js"
    format: json
    alert: ".change_24h < -20 || .change_24h > 20"
    summary: "${{.symbol}} {{.change_24h}}% ({{.price}})"

health:
  - name: disk
    command: "df -h / | tail -1 | awk '{print $5}' | tr -d '%'"
    warn: "> 80"
    critical: "> 95"

  - name: stale-working
    command: "find WORKING.md -mmin +1440 | head -1"
    alert: "!= ''"
    summary: "WORKING.md not updated in 24h"

  - name: stale-memory
    command: "find memory/ -name '*.md' -mmin -1440 | wc -l | tr -d ' '"
    alert: "== 0"
    summary: "no memory files updated today"

settings:
  timeout: 30
  parallel: true
  output: research/latest.md
```
