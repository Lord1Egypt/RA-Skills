# report-builder

Versioned OpenClaw skill for building and sending the 09:00 Telegram morning report.

## What it includes

- `SKILL.md` instructions for OpenClaw
- deterministic report payload builder
- Telegram sender with inline approval buttons
- report schema reference

## Main commands

```bash
node scripts/build_report.mjs /Users/dellymac/.openclaw/workspace/reports/latest-nightly-report.json
node scripts/send_report.mjs /Users/dellymac/.openclaw/workspace/reports/latest-nightly-report.json
```

## Expected payload

The report JSON should contain:

- `date`
- `summary`
- `reportUrl` (optional)
- `ideas`
- `infrastructureIdeas` (optional extension used locally)

## Packaging note

This folder is ready to be versioned and published through ClawHub as a skill bundle.
