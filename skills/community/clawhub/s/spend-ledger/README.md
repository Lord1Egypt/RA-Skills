# spend-ledger

Payment tracker for OpenClaw agents. Detects payments made through wallet tools, logs them to a tamper-evident local ledger, and presents them in a dashboard.

## Security

All transaction data stays on your machine:

- Log is stored at `data/transactions.jsonl`, mode `0600`
- Dashboard binds to `127.0.0.1:18920` — not reachable from the network
- Dashboard does **not** set CORS headers — a localhost-only server has no legitimate cross-origin callers; the absence of CORS prevents malicious webpages from reading your transaction data while the dashboard is open
- `service.url` stores endpoint URLs with query parameters stripped — API keys or tokens passed as query params are not written to the log
- No wallet keys or credentials are accessed — the skill observes tool call results only
- Outbound network: fetches a community-curated tool pattern list from `api.spend-ledger.com/patterns.json` daily; no payment data is included; disable with `sync_community_patterns: false` in `data/config.json`

## Configuration

Create `data/config.json` to control network behavior:

```json
{
  "sync_community_patterns": true
}
```

| Key | Default | Description |
|---|---|---|
| `sync_community_patterns` | `true` | Download tool patterns from `api.spend-ledger.com` daily; set `false` for offline/air-gapped use |

See [TECHNICAL.md](TECHNICAL.md) for the full security model, data model, and architecture.

## Install

```bash
clawhub install spend-ledger
```

Or manually:

```bash
git clone https://github.com/spend-ledger/spend-ledger.git ~/.openclaw/skills/spend-ledger
```

## Use

Ask your agent:
- "What have you spent today?"
- "Show me spending by service this week"
- "Start the budget dashboard"

Or use the CLI directly:

```bash
# Spending summary
~/.openclaw/skills/spend-ledger/scripts/query-log.sh --summary daily

# Visual dashboard at http://127.0.0.1:18920
~/.openclaw/skills/spend-ledger/scripts/dashboard.sh start

# Verify log integrity
~/.openclaw/skills/spend-ledger/scripts/query-log.sh --verify
```

## Requirements

- Node.js 18+
- OpenClaw 2026.3.x+
- No npm dependencies

## Project Structure

```
spend-ledger/
├── SKILL.md                  # Agent-facing instructions (what the LLM reads)
├── README.md                 # This file
├── TECHNICAL.md              # Architecture, security model, data model
├── openclaw.plugin.json      # Plugin manifest (id, configSchema, skills)
├── server/
│   ├── plugin.js             # Plugin entry point — registers before_tool_call and tool_result_persist hooks
│   ├── transactions.js       # Append, query, summarize, hash chain, export
│   ├── detectors.js          # Payment detection registry
│   ├── patterns-sync.js      # Community pattern sync from api.spend-ledger.com
│   ├── server.js             # HTTP server and API endpoints
│   └── index.html            # Dashboard UI (no build step, no CDN)
├── scripts/
│   ├── log-transaction.sh
│   ├── query-log.sh
│   └── dashboard.sh
├── test/
│   └── test.js               # Node built-in test runner
└── data/                     # Created at runtime, all mode 0600
    ├── transactions.jsonl
    ├── tracked-tools.json
    ├── community-patterns.json
    └── install-id.json
```

## Tests

```bash
node --test test/test.js
```

## License

MIT
