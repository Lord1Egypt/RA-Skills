---
name: ticket-signal-watch
description: Monitor ticket pages or backend ticket data for sale, restock, presale, or status-change signals; emit structured alerts that can be pushed to OpenClaw channels, webhooks, or other notification backends. Use when users want reliable ticket notifications rather than automated checkout.
metadata: {"openclaw":{"requires":{"bins":["python3"]},"emoji":"🎫"}}
---

# Ticket Signal Watch

This skill is for reliable ticket notifications, not automated checkout.

Use it when:

- a user wants to monitor ticket sale or restock signals
- a backend already has ticket data and needs a push-ready event format
- you want OpenClaw to check official pages, search pages, or other text sources for ticket signals

## Files

- Skill root: `{baseDir}`
- Script: `{baseDir}/scripts/watch_ticket_pages.py`
- Target example: `{baseDir}/config/targets.example.json`
- Notifier example: `{baseDir}/config/notifiers.example.json`
- Default state path: `{baseDir}/state/state.json`

## Operating model

Treat the workflow as three layers:

1. `collector`
   - fetch page text or consume backend data
2. `signal engine`
   - decide whether the change is meaningful
3. `notifier`
   - push the resulting event to OpenClaw channels, webhooks, or another downstream system

The ideal production setup is:

- use backend data if available
- fall back to page checks only when needed
- keep collection and notification decoupled

## Recommended usage

Run the script with a target config and a writable state file:

```bash
python3 "{baseDir}/scripts/watch_ticket_pages.py" \
  --config "{baseDir}/config/targets.example.json" \
  --state "{baseDir}/state/state.json" \
  --json
```

If `alerts` is empty, do not send a notification.

If `alerts` is non-empty, forward the structured result to:

- an OpenClaw channel
- a webhook
- a file/queue processor

## Output expectations

The script should produce:

- `results`: per-target check results
- `alerts`: only meaningful changes worth notifying
- `summary`: short human-readable summary

Each alert should contain enough information to route downstream:

- `name`
- `platform`
- `url`
- `signal_hits`
- `signal_level`
- `alert_reasons`

## Configuration guidance

Prefer official detail pages over generic search pages.

Use:

- `require_all` for identity words that must be present
- `match_any` for actionable signal words
- `signal_keywords.high` for the strongest signals

Examples of strong signals:

- `立即购买`
- `立即预订`
- `可选座`
- `有票`
- `开售`
- `预售中`
- `补票`
- `回流`
- `加场`

## Guardrails

- Do not treat generic page changes as sale signals.
- Search pages are weaker than detail pages.
- Add cooldown, dedupe, and jitter before high-frequency polling.
- If a platform starts returning anti-bot pages or challenge pages, mark that explicitly instead of claiming success.
- This skill is for notification workflows; do not imply that it can safely complete checkout automatically.
