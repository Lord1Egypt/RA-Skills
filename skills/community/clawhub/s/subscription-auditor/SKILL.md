---
name: subscription-auditor
description: >
  Personal admin: track subscriptions (cost, cycle, renewal date,
  auto-renew), see monthly/yearly totals, and get renewal reminders
  within a configurable window. Cycle math is explicit and tested;
  past-due renewals are flagged, never clamped away. All data stays
  local — nothing is sent anywhere and nothing is auto-discovered.
user-invocable: true
metadata:
  {"openclaw": {"emoji": "💳", "requires": {"bins": ["python3"], "files": [], "config": []}}}
---

# Subscription Auditor

Keeps a local ledger of subscriptions: cost, billing cycle, next
renewal, auto-renew flag, notes. `status` shows what you spend and what
renews soon; `remind` lists renewals inside the reminder window.

Ledger: `~/.openclaw/subscription-auditor/ledger.json`
(override with `SUBSCRIPTION_AUDITOR_STATE_DIR` for tests/parallel use).

## Commands

Run via bash: `~/.openclaw/plugin-skills/subscription-auditor/subscription_auditor.py <cmd> …`.
Add `--json` right after the program name for structured output.

| Command | Purpose |
|---|---|
| `add <name> --cost 15.99 [--cycle monthly] [--next-renewal YYYY-MM-DD] [--no-auto-renew] [--notes "…"]` | Add or replace a subscription (same name = replace, idempotent) |
| `list` | All entries with cycle/renewal/auto-renew |
| `status` | Totals (~X/mo, ~X/yr) + ⚠ renewals within the reminder window or past due |
| `remind [--days N]` | Renewals due within N days (default from config); includes past-due |
| `rm <id>` | Delete one entry (id = lowercased name with underscores) |
| `config` | Show/set `--remind-ahead-days N`, `--currency CODE` |

## Billing math (tested)

Every cycle converts to a yearly figure; monthly = yearly ÷ 12:

| Cycle | Yearly | Monthly |
|---|---|---|
| monthly | cost × 12 | cost |
| yearly | cost | cost ÷ 12 |
| quarterly | cost × 4 | cost × 4 ÷ 12 |
| weekly | cost × 52 | cost × 52 ÷ 12 |
| daily | cost × 365 | cost × 365 ÷ 12 |

## Behaviour rules

- **Idempotent add**: the same name replaces its previous record.
- **No invented data**: no renewal date given → defaults to today+30 and
  the output says so implicitly (`renews <date>`); the skill never
  scrapes or guesses provider billing.
- **Costs are ≥ 0**: negative costs are rejected (a negative "discount"
  entry poisons totals — that bug was fixed and has a regression test).
- **Past-due is visible**: `days_left` goes negative; status/remind
  print `PAST-DUE Nn` rather than clamping to zero.
- **Currency follows config** at add time (per-entry currency is stored,
  so changing config later doesn't rewrite history). Mixed-currency
  totals are the user's own inconsistency, not a recalculated thing.
- **Atomic writes**: ledger/config save via tmp file + rename; a
  zero-byte ledger (crash artifact) is treated as empty, not fatal.

## Example

```bash
A=~/.openclaw/plugin-skills/subscription-auditor/subscription_auditor.py
python3 $A add "IDE Rider" --cost 299 --cycle yearly --next-renewal 2026-12-01
python3 $A add Gym --cost 10 --cycle weekly
python3 $A status
python3 $A remind | sed 's/^/💳 /'
python3 $A config --currency EUR
```

## Limitations

- No payment-method tracking, no auto-discovery of bank/card charges —
  this is a manual ledger, and that's why its numbers are trustworthy.
- One currency per entry; `status` doesn't FX-convert — it sums numeric
  values and labels them with the current config currency. Keep the
  ledger single-currency (or rename cycles to include currency notes).
- Reminder window defaults to 7 days ahead; `config --remind-ahead-days`.
