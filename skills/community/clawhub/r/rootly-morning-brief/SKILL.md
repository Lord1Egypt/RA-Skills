---
name: rootly-morning-brief
description: Generate and deliver a Rootly morning incident digest for on-call operations. Use when the user asks for a daily Rootly briefing, incident summary, on-call snapshot, overdue action item report, or wants to schedule a cron-based morning ops update to Slack.
metadata:
  {
    "openclaw":
      { "requires": { "env": ["ROOTLY_API_KEY"] }, "primaryEnv": "ROOTLY_API_KEY" }
  }
---

# Rootly Morning Brief

Run `scripts/rootly_morning_brief.py` to print a short Rootly digest to stdout. OpenClaw cron `--announce` handles Slack delivery.

The output is phone-friendly by default: one line per item, Slack deep links for drill-down, and `--max-items` defaults to `3`.

## Required Inputs

- `ROOTLY_API_KEY`: Rootly API key (or a readable secret file fallback)

## Optional Inputs

- `ROOTLY_BASE_URL` (default `https://api.rootly.com`)
- `ROOTLY_TIMEZONE` (default `America/Toronto`)
- `ROOTLY_INCLUDE_PRIVATE` (`true`/`false`, default `false`)
- `ROOTLY_API_KEY_FILE` (path to a file containing only the API key)
- `ROOTLY_BRIEF_LOG_LEVEL` (`WARNING` default; set to `INFO` or `DEBUG` for troubleshooting)
- `ROOTLY_MOCK_DATA_DIR` (optional local mock data directory)

## Run Commands

Manual test:

```bash
python3 scripts/rootly_morning_brief.py
```

Include private incidents (opt-in):

```bash
python3 scripts/rootly_morning_brief.py --include-private
```

Run with local sandbox data (no Rootly account needed):

```bash
python3 scripts/rootly_morning_brief.py --mock-data-dir ./mock-data
```

Machine-readable output:

```bash
python3 scripts/rootly_morning_brief.py --json
```

## Cron Setup (Daily 8:00 AM Toronto)

```bash
openclaw cron add \
  --name "Rootly morning brief" \
  --cron "0 8 * * *" \
  --tz "America/Toronto" \
  --session isolated \
  --message "Use rootly-morning-brief. Run scripts/rootly_morning_brief.py and print the full digest." \
  --announce
```

To pin delivery to a specific Slack channel, add:
- `--channel slack --to "channel:CXXXXXXX"`

## Example stdout

```text
*Rootly Morning Brief* — Sun Mar 15
At a glance: 2 active (1 SEV0/SEV1) · 1 resolved in 24h · 2 on-call now · 1 overdue

*Active now*
• 🚨 <https://root.ly/gsif-3|Global sign-in failures after OIDC key rotation> — [SEV0] · [OPEN] · started Sun 6:42 AM
• 🟧 <https://root.ly/clsf-2|Checkout latency spike during us-east database failover> — [SEV2] · [OPEN] · started Sun 5:25 AM

*On-call now*
• Nicole Bu — L1 primary
• Jordan Patel — L2 secondary

*Overdue actions*
• ⚠️ <https://root.ly/gtb2es|Rotate CI deploy tokens and verify revocation in every production region.> — [P1] · due Sat 7:30 AM · Nicole Bu · SEC-742

*Resolved (24h)*
• <https://root.ly/ubaa-1|Unauthorized bastion access attempt blocked> — resolved Sun 12:02 AM
```

## Agent Execution Rules

1. Always run `scripts/rootly_morning_brief.py` located in the `rootly-morning-brief` skill directory; do not reimplement the digest manually.
2. Return script stdout as-is for delivery; do not paraphrase or rewrite the section structure.
3. If `--mock-data-dir` is set, run entirely from local mock files.
4. If `--mock-data-dir` is not set, use `ROOTLY_API_KEY`, then `ROOTLY_API_KEY_FILE`, then standard OpenClaw secret-file paths.
5. Use timezone `America/Toronto` unless the user asks otherwise.
6. Default to public-only incidents.
7. Only include private incidents if the user explicitly opts in.
8. Keep output short and readable on a phone screen.
9. If one section has no data, include a clear "none" line instead of omitting the section.
