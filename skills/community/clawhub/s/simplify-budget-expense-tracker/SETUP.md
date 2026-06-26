# Setup

This is the shortest reliable setup for a real user.

## Before You Start

You must use this exact template, or a direct copy of it:
- [Simplify Budget Template](https://docs.google.com/spreadsheets/d/1fA8lHlDC8bZKVHSWSGEGkXHNmVylqF0Ef2imI_2jkZ8/edit?gid=524897973#gid=524897973)

If you use a different budget sheet, this skill will not work.

## 1. Copy The Template

Make your own copy of the template in Google Sheets.

Your copy must still contain:
- `Expenses`
- `Income`
- `Recurring`
- `Dontedit`

Do not change the expected column layout unless you also change the scripts.

Set a canonical OpenClaw root first:

```bash
export OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
```

## 2. Install The Skill

Put this skill at:

```bash
$OPENCLAW_HOME/skills/simplify-budget
```

## 3. Use The Bundled Command Wrappers

For Telegram and OpenClaw command routing, use the bundled command wrappers at:

```bash
$OPENCLAW_HOME/skills/simplify-budget/commands
```

The bundled command layer has two parts:

**`exec.sh`** — the central dispatcher all wrappers call. It handles:
- argument normalisation (`--date`, `--amount`, `--account`, etc.)
- date parsing: converts natural language like `"yesterday"`, `"2 days ago"`, `"March 31"` into `YYYY-MM-DD` automatically
- category resolution: fuzzy-matches a description to the hardcoded category list
- category cache: reads `$OPENCLAW_HOME/cache/simplify-budget/categories.tsv` so inactive categories work without hitting the sheet

**`log.sh`** — natural language expense entry, the recommended command for Telegram. Pass the user's full expense message as one raw string. Optional account/date should only be passed when they are independently clear:
```bash
./log.sh "i bought the pencil for 10 euro and i want you to log it to business category"
./log.sh "Shell 12.50" "Revolut" "yesterday"
./log.sh "dentist 80 euro" "Revolut" "March 31"
```
Do not ask the user to rephrase into CLI-shaped chunks like `"pencil 10 euro"`. The date phrase (`"yesterday"`, `"2 days ago"`, `"March 31"`, `"last week"`) is parsed by `exec.sh` — the bot never needs to compute or pass an ISO date itself.

**Thin shell wrappers** — one per script, each forwards to `exec.sh`. These are bundled in `$OPENCLAW_HOME/skills/simplify-budget/commands`:
```
write_expense.sh    update_expense.sh    delete_expense.sh    find_expenses.sh
write_income.sh     update_income.sh     delete_income.sh     find_income.sh
write_recurring.sh  update_recurring.sh  delete_recurring.sh  find_recurring.sh
find_summary.sh     get_categories.sh    monthly_totals.sh
income_this_month.sh  spending_this_month.sh  savings_this_month.sh
add_subscription.sh   update_subscription.sh  delete_subscription.sh
list_subscriptions.sh  check_subscriptions.sh  log_subscription.sh
```

Each thin wrapper looks like this (adjust the script name):
```bash
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "${SCRIPT_DIR}/exec.sh" write_expense.sh "$@"
```

Without the bundled command wrappers the skill files still exist, but the bot will have no reliable way to route commands, resolve dates, or match categories.

## 4. Create Or Reuse A Google Service Account

Create a Google Cloud service account with Google Sheets access and download the JSON key.

A common location is:

```bash
$OPENCLAW_HOME/sa.json
```

## 5. Share The Sheet With The Service Account

Open your copied Google Sheet and share it with the service account email from the JSON key.

Give it editor access.

If you skip this, reads and writes will fail.

## 6. Set Environment Variables

Add these to your OpenClaw config or shell environment:

```bash
export GOOGLE_SA_FILE="$OPENCLAW_HOME/sa.json"
export SPREADSHEET_ID="your_google_sheet_id"
export TRACKER_CURRENCY="EUR"
export TRACKER_CURRENCY_SYMBOL="€"
```

Required:
- `GOOGLE_SA_FILE`
- `SPREADSHEET_ID`
- `TRACKER_CURRENCY`

Optional:
- `TRACKER_CURRENCY_SYMBOL`

## 7. Verify The Template Assumptions

The skill expects:
- active categories in `Dontedit!L10:O39`
- `Expenses` ledger starts at row `5`
- `Income` ledger starts at row `5`
- `Recurring` ledger starts at row `6`
- expense and recurring expense categories use `=zategory<stableId>`
- recurring income uses `Income 💵`

## 8. Restart OpenClaw

```bash
openclaw daemon restart
```

If Telegram is already connected, restart after config changes so it picks up the new environment and bundled command wrappers.

## 9. Smoke Test

Expense via natural language (recommended):

```bash
bash "$OPENCLAW_HOME/skills/simplify-budget/commands/log.sh" "setup test 10 euro" "Cash"
```

Expense via explicit flags:

```bash
bash "$OPENCLAW_HOME/skills/simplify-budget/commands/write_expense.sh" \
  --amount 10 \
  --category 4 \
  --description "setup test" \
  --date "$(date +%Y-%m-%d)" \
  --account Cash
```

Recurring:

```bash
bash "$OPENCLAW_HOME/skills/simplify-budget/commands/write_recurring.sh" \
  --start-date 2026-03-28 \
  --name "setup recurring test" \
  --category "Business 💻️" \
  --type expense \
  --frequency Monthly \
  --amount 10 \
  --account Cash
```

Delete the test rows afterward.

## 10. Telegram

If the user wants Telegram access too:
- configure the Telegram bot token in OpenClaw
- use pairing or allowlist
- make sure the Telegram prompt routes budget requests to the bundled Simplify Budget command wrappers

This repo does not contain any private Telegram token or local OpenClaw config.

## Common Failures

`scripts are missing`
- the skill was not installed correctly, or the bundled command wrappers are missing

`category not found`
- the user is not using the real template, or the category table changed

`writes go to wrong rows`
- the user changed the template layout

`Google Sheets auth failure`
- the sheet was not shared with the service account

`transaction not found`
- the bot guessed the wrong row; use a more specific query
