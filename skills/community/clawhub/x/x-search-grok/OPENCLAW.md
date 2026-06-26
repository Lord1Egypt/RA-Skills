# x-search — OpenClaw Scheduled Use

Use OpenClaw's built-in cron scheduler to run x-search automatically on a schedule and push results to your messaging platform.

## Schedule formats

| Type | Parameter | Example |
|------|-----------|---------|
| Recurring (interval) | `--every` | `--every 24h` |
| Recurring (cron expr) | `--cron` + `--tz` | `--cron "0 8 * * *" --tz "Asia/Shanghai"` |
| One-shot | `--at` | `--at "2026-03-23T08:00:00Z"` |

Always use `--session isolated` for scheduled tasks — each run gets its own sandboxed session.

For watchlist runs, add `--progress-only` to prevent full Markdown from being injected into the agent context (significantly reduces token consumption):
```bash
python3 watchlist.py --time 24h --lang zh --output ~/obsidian/X/ --progress-only
```

---

## Scenario 1: Daily account monitoring

**Natural language mode** — the agent interprets and runs the skill:
```bash
openclaw cron add \
  --name "karpathy-daily" \
  --cron "0 8 * * *" --tz "Asia/Shanghai" \
  --session isolated \
  --message "Search X for @karpathy's posts in the last 24 hours, save to ~/obsidian/X/" \
  --announce --channel telegram --to "your-chat-id"
```

**Slash command mode** — direct CLI invocation:
```bash
openclaw cron add \
  --name "karpathy-daily" \
  --cron "0 8 * * *" --tz "Asia/Shanghai" \
  --session isolated \
  --message "/x-search --output ~/obsidian/X/ account @karpathy --time 24h" \
  --announce --channel telegram --to "your-chat-id"
```

Multiple accounts:
```bash
--message "/x-search --output ~/obsidian/X/ account @karpathy @sama @elonmusk --time 24h"
```

---

## Scenario 2: Daily trending topics

**Natural language mode:**
```bash
openclaw cron add \
  --name "tech-trends-daily" \
  --cron "0 9 * * 1-5" --tz "Asia/Shanghai" \
  --session isolated \
  --message "Search X for the top trending posts about #AI and #LLM today, save to ~/obsidian/X/" \
  --announce --channel telegram --to "your-chat-id"
```

**Slash command mode:**
```bash
openclaw cron add \
  --name "tech-trends-daily" \
  --cron "0 9 * * 1-5" --tz "Asia/Shanghai" \
  --session isolated \
  --message "/x-search --output ~/obsidian/X/ trends '#AI' '#LLM'" \
  --announce --channel telegram --to "your-chat-id"
```

---

## Scenario 3: Real-time topic search (on-demand)

No cron needed — trigger directly in OpenClaw chat:

**Natural language:**
> "Search X for hot discussions about crude oil price predictions this week"

**Slash command:**
```
/x-search topic "crude oil price prediction"
/x-search --output ~/obsidian/X/ topic "Claude MCP"
```

---

## Delivery channels

Replace `--channel telegram --to "your-chat-id"` with your platform:

| Platform | Example |
|----------|---------|
| Telegram | `--channel telegram --to "123456789"` |
| Slack | `--channel slack --to "channel:C1234567890"` |
| Discord | `--channel discord --to "channel:987654321"` |

---

## Managing cron jobs

```bash
openclaw cron list                              # list all jobs
openclaw cron delete --name "karpathy-daily"   # remove a job
openclaw cron pause  --name "karpathy-daily"   # pause without deleting
```
