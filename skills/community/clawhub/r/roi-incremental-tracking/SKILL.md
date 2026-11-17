---
name: roi-incremental-tracking
description: Track your AI agent's ROI incrementally — log time saved and direct cash as deliveries happen, then close the cycle monthly with an HTML dashboard.
---

# Incremental ROI Tracking

Use this skill when the user asks to measure, log, or close out the agent's ROI / value cycle.

## Purpose

Measure the value the agent generates **incrementally, as deliveries happen**, instead of reconstructing it from memory at the end of the month. One lightweight ledger row per relevant delivery; a monthly closeout turns the ledger into numbers and a dashboard.

## Files

All tracking data lives in `<workspace>/reports/roi/`:

| File | Role |
| --- | --- |
| `config.json` | User parameters (cost, hourly value, currency, cycle day) |
| `ledger-current.csv` | Incremental ledger for the current cycle |
| `monthly-summary.csv` | One row per closed cycle |
| `render_roi_report.py` | Dashboard generator (copied from this skill's `scripts/` folder) |
| `index.html` | Static HTML dashboard, regenerated at closeout |

## First-run setup

If `<workspace>/reports/roi/config.json` does not exist, run setup before anything else:

1. Ask the user for:
   - **Monthly cost** of running the agent (subscription + API + infra), a single number.
   - **Currency** symbol or code (e.g. `USD`, `EUR`, `R$`).
   - **Base hourly value** of the user's time — the conservative rate used to price minutes saved.
   - Optional **alternative hourly scenarios** (e.g. 50, 100, 180) kept for comparison only.
   - **Cycle start day** (1–28). The cycle runs from that day to the day before it in the next month. Default: 1.
2. Save the answers to `config.json`:

```json
{
  "monthly_cost": 100.0,
  "currency": "USD",
  "base_hourly_value": 25.0,
  "alternative_hourly_scenarios": [50, 100],
  "cycle_start_day": 1
}
```

3. Create `ledger-current.csv` containing only the header row (see **Ledger fields**).
4. Copy `render_roi_report.py` from this skill's `scripts/` directory into `<workspace>/reports/roi/`.

## Rules

- Do **not** run heavy continuous collection for ROI. This skill costs almost nothing to maintain.
- Add **one ledger row only when a relevant delivery happens** (task automated, report produced, problem caught, deal supported).
- Use **conservative** minutes saved. When in doubt, estimate low.
- Count direct cash **only when confirmed with a closed value** (invoice paid, discount obtained, refund recovered). Never count pipeline or expected revenue.
- Keep **risk avoided as narrative** unless the user explicitly authorizes a monetary assumption.
- If an estimate is uncertain, set `include_in_closeout=no` until the user reviews it.

## Ledger fields

```
date,cycle_start,cycle_end,title,category,minutes_saved,cash_direct,confidence,evidence,include_in_closeout,notes
```

- `date` — ISO date of the delivery (YYYY-MM-DD).
- `cycle_start` / `cycle_end` — ISO dates of the cycle this row belongs to (derived from `cycle_start_day`).
- `title` — short name of the delivery.
- `category` — free tag (e.g. `automation`, `report`, `support`, `sales`).
- `minutes_saved` — conservative integer estimate; 0 if none.
- `cash_direct` — confirmed cash in the configured currency; 0 if none.
- `confidence` — `high` | `medium` | `low`.
- `evidence` — where proof lives (message link, file path, ticket id).
- `include_in_closeout` — `yes` | `no`.
- `notes` — anything else.

## Monthly closeout

At the end of each cycle (when the current date reaches `cycle_start_day` again, or when the user asks):

1. Append one summary row for the cycle to `monthly-summary.csv` with the header:

```
cycle_start,cycle_end,entries,minutes_saved,hours_value,cash_direct,total_value,monthly_cost,roi_cash_only,roi_cash_plus_hours,notes
```

   where `hours_value = minutes_saved / 60 * base_hourly_value`, `total_value = cash_direct + hours_value`, and ROI values are `value / monthly_cost` (only rows with `include_in_closeout=yes` count).

2. Regenerate the dashboard:

```bash
python3 <workspace>/reports/roi/render_roi_report.py
```

3. Start a fresh `ledger-current.csv` for the new cycle (archive the old one as `ledger-<cycle_start>.csv` if the user wants history).

4. Report to the user:
   - **Cash-only ROI** (confirmed cash vs monthly cost);
   - **Cash + base-hour ROI** (cash plus priced minutes vs monthly cost);
   - Comparison against the previous month;
   - Dashboard location (`index.html`);
   - **Major risks avoided and persistent assets** created, narrated separately from money.

Once multiple closed months exist, the dashboard's multi-month chart becomes the trend view — use it in the report.
