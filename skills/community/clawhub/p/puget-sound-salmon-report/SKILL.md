---
name: "puget-sound-salmon-report"
description: "Scrape WDFW Puget Sound creel data into salmon CPUE reports: daily digest, weekly top-launch email with chart, and proactive hot-bite alerts."
---

# Puget Sound Salmon Creel Report

Turn WDFW's [Puget Sound creel reports](https://wdfw.wa.gov/fishing/reports/creel/puget)
into actionable salmon fishing intel: per-area catch-per-angler (CPUE), trends, the best
boat launches this week, a chart, an emailable digest, and optional proactive "hot bite"
alerts. Pick any of the 5 Pacific salmon and any marine areas.

## When to use

Use when a user wants to track recreational salmon catch/effort for Puget Sound marine
areas — "how's the coho bite in Area 10", "email me the best launches Friday", "alert me
when fishing spikes". The quantitative core is deterministic Python (trustworthy numbers);
there is no LLM in the data path.

## Setup

```bash
pip install --user matplotlib   # only needed for the weekly chart; everything else is stdlib
```

The script is `scripts/creel_report.py`. Copy `templates/config.json` next to it (or pass
`--config PATH`) to choose species/areas/thresholds. CLI flags override the config file.

## Configure (`config.json`)

- `areas` — marine area codes as shown on WDFW (e.g. `"8-2","9","10","11"`).
- `species` — any of `chinook, coho, chum, pink, sockeye`; multiple are combined into one CPUE.
- `trailing_days` — days re-scraped each run (WDFW revises data after QA/QC).
- `top_launches`, `min_week_anglers` — weekly launch ranking size + sample floor.
- `until` — `"YYYY-MM-DD"`; `--email` stops on/after this date (for time-boxed seasons).
- `alerts` — proactive hot-bite watcher (see below).

## Usage

```bash
python3 creel_report.py                       # daily per-area digest -> stdout
python3 creel_report.py --weekly              # weekly top-launch report + chart -> stdout
python3 creel_report.py --weekly --email      # HTML email with embedded chart
python3 creel_report.py --watch               # proactive hot-bite alert, or "NO_ALERT"
python3 creel_report.py --species chum,coho --areas 9,10 --weekly
python3 creel_report.py --no-fetch ...        # use stored data, skip scraping
```

## Scheduling

Frequency = how often you schedule the mode. Any scheduler works (cron, launchd, or an
OpenClaw cron job). Example crontab:

```cron
30 8 * * *   python3 creel_report.py                                  # daily digest
0  9 * * 5   python3 creel_report.py --weekly --email --until 2026-09-25
0  12,17 * * * python3 creel_report.py --watch                        # hot-bite checks
```

## Email (optional)

`--email` reads SMTP creds from `~/.openclaw/creel_email.json` (never commit it):

```json
{
  "smtp_host": "smtp.gmail.com", "smtp_port": 465,
  "smtp_user": "you@gmail.com", "smtp_pass": "APP_PASSWORD",
  "from": "you@gmail.com",
  "to": ["you@example.com"],
  "bcc": ["friend@example.com"],
  "subscribers_url": "",        // published Google Sheet CSV (Google Form signups) -> merged into bcc
  "unsubscribe_url": "",        // published CSV of opt-outs -> removed from every send
  "subscribe_form_url": "", "unsubscribe_form_url": ""   // footer links
}
```

For Gmail use an App Password. `to`/`cc`/`bcc` accept a string, comma-string, or list. A
published Google Form → Sheet gives a self-serve signup UI: put the CSV link in
`subscribers_url` and every email-looking cell is merged into BCC (de-duped); `unsubscribe_url`
removes opt-outs (your own `to` is always kept). The chart embeds via a `cid:` attachment so it
renders in Outlook.

## Proactive hot-bite alerts (`--watch`)

`--watch` flags when the latest day's CPUE in an area spikes vs its recent baseline, else
prints `NO_ALERT`. **Toggle with `alerts.enabled`.** It's self-limiting — a state file
(`memory/creel/alert_state.json`) plus a cooldown means an area won't re-alert until the
cooldown passes or the bite gets meaningfully hotter.

```json
"alerts": {
  "enabled": true, "spike_mult": 1.8, "min_anglers": 30,
  "min_cpue": 0.4, "cooldown_days": 2, "min_baseline_days": 2
}
```

Wire delivery so a bare `NO_ALERT` posts nothing. This pairs naturally with an agent runtime
(e.g. OpenClaw heartbeat/cron) that can message you proactively; with plain cron, gate on the
output: `out=$(python3 creel_report.py --watch); [ "$out" = NO_ALERT ] || notify "$out"`.

## Data / output

Written under `memory/creel/` relative to the script: `daily.json` (ramp-level history, all
species), `cpue_areas.png`, `latest_digest.md`, `weekly_report.md`, `alert_state.json`.

## Notes / limitations

- WDFW publishes no public API for the marine areas; this scrapes the server-rendered HTML
  table, so a major page redesign could require updating the parser.
- Same-day data is partial until WDFW fills it in overnight; the digest anchors on the latest
  substantially-sampled day.
- Quotas/closures are not tracked (Coho isn't quota-managed); check WDFW regs before fishing.
