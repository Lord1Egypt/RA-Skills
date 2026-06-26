# Token Burn Monitor — API Reference

Base URL: `http://localhost:3847` (configurable via `config.json` or `PORT` env)

All endpoints return JSON. GET-only. Server binds to `127.0.0.1` by default — no cross-origin requests are served.

## Endpoints

### GET /api/config

Agent configuration (names, icons). Frontend uses this to render agent cards.

**Response:**
```json
{
  "agents": {
    "main": { "name": "Main Agent", "icon": null },
    "helper": { "name": "Helper", "icon": "/assets/helper.png" }
  }
}
```

- Agents are auto-discovered from the agents directory
- `config.json` overrides display name and icon
- `icon: null` means no custom icon (frontend should generate one)

---

### GET /api/stats?date=YYYY-MM-DD

Aggregated stats for all agents on a given date. Defaults to today.

**Response:**
```json
{
  "date": "2026-03-10",
  "timestamp": "2026-03-10T08:00:00.000Z",
  "agents": {
    "main": {
      "agentId": "main",
      "totalTokens": 150000,
      "inputTokens": 50000,
      "outputTokens": 20000,
      "cacheReadTokens": 70000,
      "cacheWriteTokens": 10000,
      "reasoningTokens": 0,
      "totalCost": 2.50,
      "inputCost": 0.75,
      "outputCost": 1.50,
      "cacheReadCost": 0.10,
      "cacheWriteCost": 0.15,
      "messageCount": 42,
      "queryCount": 15,
      "models": {
        "anthropic/claude-opus-4-6": {
          "tokens": 150000,
          "cost": 2.50,
          "messages": 42,
          "provider": "Anthropic"
        }
      },
      "latestStatus": {
        "contextLength": 130000,
        "cacheHitRate": "53.8",
        "lastModel": "anthropic/claude-opus-4-6",
        "lastTimestamp": "2026-03-10T07:55:00.000Z"
      }
    }
  },
  "totals": {
    "totalTokens": 150000,
    "inputTokens": 50000,
    "outputTokens": 20000,
    "cacheReadTokens": 70000,
    "cacheWriteTokens": 10000,
    "reasoningTokens": 0,
    "totalCost": 2.50,
    "inputCost": 0.75,
    "outputCost": 1.50,
    "cacheReadCost": 0.10,
    "cacheWriteCost": 0.15,
    "messageCount": 42,
    "queryCount": 15
  }
}
```

---

### GET /api/agent/:id?date=YYYY-MM-DD

Detailed breakdown for a single agent, including per-call messages.

**Response:** Same fields as the agent entry in `/api/stats`, plus:

```json
{
  "messages": [
    {
      "timestamp": "2026-03-10T07:55:00.000Z",
      "model": "anthropic/claude-opus-4-6",
      "provider": "Anthropic",
      "input": 5000,
      "output": 2000,
      "cacheRead": 45000,
      "cacheWrite": 0,
      "reasoning": 0,
      "totalTokens": 52000,
      "cost": 0.12,
      "inputCost": 0.075,
      "outputCost": 0.03,
      "cacheReadCost": 0.0045,
      "cacheWriteCost": 0,
      "toolCallCount": 3,
      "toolNames": ["exec", "read", "write"],
      "userPrompt": "[redacted]"
    }
  ]
}
```

**`userPrompt`:** Redacted by default (shows `"[redacted]"`). When `showPrompts` is enabled in config, shows the user message that triggered this response (truncated to 300 chars). Extracted from session files with Feishu/system envelope stripped. `null` if no user message found.

---

### GET /api/history?days=N

Cost history for the last N days (default 30).

**Response:**
```json
{
  "history": [
    {
      "date": "2026-03-10",
      "totalCost": 5.20,
      "totalTokens": 500000,
      "messageCount": 120,
      "queryCount": 45,
      "agents": {
        "main": { "totalCost": 4.00, "totalTokens": 400000, "messageCount": 100 },
        "helper": { "totalCost": 1.20, "totalTokens": 100000, "messageCount": 20 }
      }
    }
  ]
}
```

---

### GET /api/pricing

Model pricing table ($ per 1M tokens).

**Response:**
```json
{
  "anthropic/claude-opus-4-6": {
    "input": 15, "output": 75,
    "cacheRead": 1.5, "cacheWrite": 18.75,
    "provider": "Anthropic"
  }
}
```

---

### GET /api/crons

Scheduled cron jobs grouped by executing agent.

**Response:**
```json
{
  "byAgent": {
    "main": [
      {
        "id": "job-id",
        "name": "Job Name",
        "brief": "Task description",
        "scheduleHuman": "Every 30 min",
        "scheduleRaw": "*/30 * * * *",
        "scheduleKind": "cron",
        "triggerAgent": "main",
        "executingAgent": "main",
        "sessionTarget": "isolated",
        "enabled": true,
        "lastRunAt": "2026-03-10T07:30:00.000Z",
        "lastStatus": "ok",
        "lastDurationMs": 5200,
        "nextRunAt": "2026-03-10T08:00:00.000Z",
        "consecutiveErrors": 0
      }
    ]
  },
  "total": 5
}
```

---

### GET /api/cron/:jobId/runs

Run history for a specific cron job.

**Response:**
```json
{
  "runs": [
    {
      "runAtMs": 1710000000000,
      "status": "ok",
      "durationMs": 5200,
      "nextRunAtMs": 1710001800000
    }
  ],
  "total": 10
}
```

---

## Theme Development

Themes are directories under `themes/`. Set `"theme": "my-theme"` in config.json.

A theme directory needs at minimum:
- `index.html` — served at `/`

Optional:
- `assets/` — served at `/assets/*` (images, CSS, JS)

The theme fetches all data from the API endpoints above. See `themes/default/` for reference implementation.

### Security

- HTML responses include a `Content-Security-Policy` header restricting `connect-src` and `font-src` to `'self'` only — themes cannot make external network requests.
- Static file serving is sandboxed to the theme directory (path traversal protected).
- The default theme makes zero external requests (system fonts only, no CDN loads).
- Review any custom or third-party theme before enabling.
