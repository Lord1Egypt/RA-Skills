---
name: receipt-warranty-tracker
description: >
  Personal admin: photograph a receipt, it stores the item, price, and
  warranty end date, then reminds you before coverage lapses.
user-invocable: true
metadata:
  {"openclaw": {"emoji": "🧾", "requires": {"bins": ["python3"], "files": [], "config": []}}}
---

# Receipt & Warranty Tracker

Snaps a receipt, it stores item/price/warranty end; the skill reminds you
before coverage lapses. All data stays on disk — nothing is sent anywhere.

Ledger: `~/.openclaw/receipt-warranty-tracker/ledger.json` (override the
whole state dir with `RECEIPT_WARRANTY_STATE_DIR` for tests or parallel
instances).

## Commands

Run via bash: `~/.openclaw/plugin-skills/receipt-warranty-tracker/receipt_warranty.py <cmd> …`.
Add `--json` right after the program name for structured output.

| Command | Purpose |
|---|---|
| `add --item X --receipt "…" --price 12.99 --warranty-days 365` | Store a receipt+item. Repeatable as many times as you like. |
| `add --item X --warranty-until 2027-05-01` | Store when you already know the coverage end. Invalid dates are rejected. |
| `status` | Per-entry state: ok / REMIND / EXPIRED / no-warranty, with days-left. |
| `remind` | Mark today's reminders and save the flag (no duplicates). |
| `list` | Simple registry: item / price / warranty days / warranty-until. |
| `rm <item>` | Delete one entry. |
| `estimate --date 2026-10-01 --days 3650` | Estimate warranty end for already-bought items you haven't entered. |
| `config [--remind-ahead-days N]` | Show/set how many days ahead reminders fire. |

## Behaviour rules

- **Idempotent add**: the same item name replaces its previous record.
- **Price is unitless money here** — you write the amount, the skill
  neither formats nor interprets it; use `--currency` to tag it.
- **Reminder policy**: `remind` fires when `warranty_until − today ≤
  remind_ahead_days`. `remind_ahead_days` is config (`config
  --remind-ahead-days N`, default 3). Once `remind` has fired for an
  entry, it won't echo again until you delete or edit it.
- **Expiry semantics**: `status` and `remind` classify entries past their
  warranty end as `EXPIRED` (checked against `date.today()`).
- **Never invent coverage**: without `--warranty-days` or
  `--warranty-until`, entries carry no warranty window — the skill tells
  you so explicitly instead of guessing.
- **Atomic writes; file lock unused**: ledger saves lock briefly via tmp
  file + rename; concurrent CLI runs are effectively serialized by the
  atomic replace (the fcntl lock file is no longer used).

## Example

```bash
R=~/.openclaw/plugin-skills/receipt-warranty-tracker/receipt_warranty.py
python3 $R add --item "MacBook Pro 14" --receipt "photo: 4 lines, $2499" \
  --price 2499 --warranty-days 365
python3 $R status
python3 $R remind | sed 's/^/🧾 /'
```
