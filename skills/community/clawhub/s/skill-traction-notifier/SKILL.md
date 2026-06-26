---
name: Skill Surge Notifier
slug: skill-surge-notifier
version: 0.1.0
author: "@gkauf_gm"
tags: [monitoring, clawhub, acceleration, meta]
homepage: https://github.com/Gabriel-Kaufman/skill-scraper/tree/main
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["node"]}}}
---

# Skill Surge Notifier

Monitors ClawHub for skills gaining traction. Tracks download and star counts over time and alerts when a skill is surging.

A surge is triggered when any of these are true:
- Download growth >30% since last check
- Total downloads >50,000
- Stars >200
- A new skill appeared in the top 10

---

## Setup

Requires Node.js 18+. No install needed — runs directly from the skill bundle.

---

## Commands

| Command | What it does |
|---|---|
| `node {baseDir}/cli.js fetch` | Show top 20 skills by downloads |
| `node {baseDir}/cli.js check` | Run surge detection, top movers, and update state |
| `node {baseDir}/cli.js status` | Last check, thresholds, notification status |
| `node {baseDir}/cli.js profile` | Show current agent profile |
| `node {baseDir}/cli.js profile set "description" "kw1,kw2"` | Set profile for relevance scoring |
| `node {baseDir}/cli.js config movers=5` | Set number of top movers shown |
| `node {baseDir}/cli.js config movers-off` | Disable top movers |
| `node {baseDir}/cli.js config growth=30 downloads=50000 stars=200` | Update surge thresholds |

Every `check` run always shows top N movers (by download delta) regardless of thresholds, so there's always something to look at.

When a profile is set, surges are scored 0-10 for relevance and sorted accordingly — most relevant first.

---

## Notes

- State is stored in `~/.skill-surge-notifier/state.json`. The first run seeds the baseline; growth % appears from the second run onward.
- All output is printed to stdout. When used inside an agent, the agent must capture the CLI output to surface alerts in chat.
- To run automatically, add to crontab (`crontab -e`):

```bash
0 */4 * * * node {baseDir}/cli.js check >> ~/.skill-surge-notifier/surge.log 2>&1
```

## Environment Variables

These optional env vars override default paths and behavior:

| Variable | Default | Description |
|---|---|---|
| `SURGE_DIR` | `~/.skill-surge-notifier` | Base directory for all state and config files |
| `STATE_PATH` | `$SURGE_DIR/state.json` | Path to the skill state file |
| `CONFIG_PATH` | `$SURGE_DIR/config.json` | Path to the config file |
| `SCHEDULED` | `false` | Set to `true` when running from a scheduler; adds a random 1–5 min delay before fetching to spread API load |
