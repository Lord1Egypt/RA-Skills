---
name: revenue-dashboard
description: Track revenue across multiple Stripe accounts with automated daily reports, goal tracking, and anomaly alerts. Use when checking revenue, running nightly reviews, comparing periods, tracking MRR/ARR, detecting revenue anomalies, or answering any revenue or sales performance question. Triggers on revenue, Stripe metrics, MRR, ARR, daily review, sales numbers, growth rate, churn, or financial dashboard.
---

# Revenue Dashboard

Consolidated revenue intelligence across your Stripe accounts. Pulls charges, refunds, subscriptions, and MRR in a single command with period-over-period comparison, goal tracking, and anomaly detection.

## Quick Start

1. Store your Stripe secret key at `~/.config/stripe/api_key`
2. Copy the config template and edit it:
   ```bash
   cp {baseDir}/references/config-template.json ~/.config/revenue-dashboard/config.json
   ```
3. Edit `~/.config/revenue-dashboard/config.json` with your Stripe account IDs and revenue goals
4. Run your first report:
   ```bash
   python3 {baseDir}/scripts/revenue.py --period today
   ```

## Commands

### Revenue Report
```bash
python3 {baseDir}/scripts/revenue.py --period <period> [--format <format>]
```

**Periods:** `today`, `yesterday`, `week`, `month`, `quarter`, `year`, `all`
**Formats:** `json` (default), `markdown`, `summary`

### Goal Tracking
```bash
python3 {baseDir}/scripts/revenue.py --period month --goals
```

Shows progress toward your monthly and annual revenue targets defined in config.

### MRR & Subscription Metrics
```bash
python3 {baseDir}/scripts/mrr.py [--breakdown]
```

Pulls active subscriptions across all accounts. With `--breakdown`, groups by plan/price.

### Anomaly Detection
```bash
python3 {baseDir}/scripts/revenue.py --period today --anomalies
```

Flags unusual activity: revenue spikes/drops >2x vs 7-day average, refund rate >10%, or zero-revenue days.

## Nightly Review Workflow

Run this sequence for a complete daily close:

```bash
# 1. Yesterday's final numbers
python3 {baseDir}/scripts/revenue.py --period yesterday --format markdown --goals --anomalies

# 2. Monthly trend context
python3 {baseDir}/scripts/revenue.py --period month --format summary

# 3. Current MRR snapshot
python3 {baseDir}/scripts/mrr.py --breakdown
```

Write findings to your daily notes. Propose next-day actions based on what the numbers show.

### Automated Nightly Cron

```json
{
  "name": "nightly-revenue",
  "schedule": {"kind": "cron", "expr": "0 3 * * *", "tz": "America/Los_Angeles"},
  "sessionTarget": "main",
  "payload": {
    "kind": "systemEvent",
    "text": "Run the nightly revenue review using the revenue-dashboard skill. Pull yesterday's revenue, check goals, flag anomalies, and propose tomorrow's plan."
  }
}
```

## Configuration

See `references/config-template.json` for the full config schema. Key fields:

```json
{
  "accounts": {
    "my_saas": "acct_XXXXXXXXXXXX",
    "my_shop": "acct_YYYYYYYYYYYY"
  },
  "goals": {
    "monthly": 10000,
    "annual": 120000
  },
  "currency": "usd",
  "anomaly_threshold": 2.0
}
```

## Key Metrics Tracked

- **Gross / Net Revenue** per account and consolidated
- **Refund rate** as percentage of gross
- **Transaction count** and average ticket size
- **Period-over-period growth %** with directional indicator
- **MRR / ARR** from active subscriptions
- **Goal progress** as percentage with projected monthly/annual totals
- **Anomaly flags** for unusual patterns

## Interpreting Output

- **Growth > 0%**: Revenue accelerating vs prior period
- **Refund rate > 5%**: Investigate product or fulfillment issues
- **MRR trend**: The most important metric for subscription businesses
- **Goal pace**: "On pace" means current run rate meets the target; "Behind" means action needed

## Multi-Account Strategy

Add as many Stripe accounts as you operate. The dashboard consolidates everything but preserves per-account detail so you can see which products drive growth. Common setups:

- **SaaS + info products**: Track subscription MRR alongside one-time course/template sales
- **Multiple brands**: See consolidated revenue while monitoring each brand independently
- **Marketplace + services**: Separate platform fees from direct service revenue
