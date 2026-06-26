---
name: ynab-api
description: "YNAB (You Need A Budget) budget management via API. Add transactions, track goals, monitor spending, create transfers, and generate budget reports. Use this skill whenever the user mentions YNAB, budget tracking, spending analysis, budget goals, Age of Money, or wants to manage their personal finances -- even if they just say 'add an expense', 'how much did I spend', 'check my budget', or 'upcoming bills' without naming YNAB explicitly. Also use for automated budget reports and financial summaries."
user-invocable: true
metadata: {"requiredEnv": ["YNAB_API_KEY", "YNAB_BUDGET_ID"]}
---

# YNAB Budget Management

Manage your YNAB budget via the API with ready-to-use bash scripts. Requires `curl` and `jq`.

## Configuration

Set environment variables `YNAB_API_KEY` and `YNAB_BUDGET_ID`, or create `~/.config/ynab/config.json`:

```json
{
  "api_key": "YOUR_YNAB_TOKEN",
  "budget_id": "YOUR_BUDGET_ID",
  "monthly_target": 2000
}
```

The `monthly_target` field sets your monthly spending cap (used by `daily-spending-report.sh`). Can also be set via `YNAB_MONTHLY_TARGET` env var.

Get your token at https://app.ynab.com/settings/developer. Find your Budget ID in the YNAB URL.

## Available Scripts

All scripts are in `{baseDir}/scripts/` and output to stdout.

| Script | Purpose |
|--------|---------|
| `daily-spending-report.sh` | Yesterday's expenses by category + monthly budget progress + analysis |
| `daily-budget-check.sh` | Morning overview: Age of Money, upcoming bills, overspending alerts |
| `goals-progress.sh [month]` | Visual progress bars for category goals |
| `scheduled-upcoming.sh [days]` | Upcoming scheduled transactions (default: 7 days) |
| `month-comparison.sh [m1] [m2]` | Month-over-month spending comparison |
| `transfer.sh SRC DEST AMT DATE [MEMO]` | Create a properly linked account transfer |
| `ynab-helper.sh <command>` | General helper: search payees, list categories, add transactions |
| `setup-automation.sh` | Test config and list available scripts |

## Key API Concepts

### Amounts use milliunits
YNAB API represents all amounts in milliunits: `10.00` = `10000`, `-10.00` = `-10000`. Always divide by 1000 when displaying, multiply by 1000 when submitting.

### Always categorize transactions
Never create transactions without a category -- it breaks budget tracking. When encountering an unfamiliar merchant, search past transactions for the same payee and reuse the category for consistency.

### Check for pending transactions before adding
Before creating a new transaction, check if an unapproved one already exists for the same amount. If found, approve it instead. This avoids duplicates from bank imports.

### Transfers require transfer_payee_id
To create a real linked transfer between accounts, use the destination account's `transfer_payee_id` (not `payee_name`). Using `payee_name` creates a regular transaction that YNAB won't recognize as a transfer. See [references/api-guide.md](references/api-guide.md) for the full transfer guide.

### Split transactions
Transactions with category "Split" contain `subtransactions`. Always expand them to show subcategories in reports -- never show "Split" as a category name.

## Common API Operations

```bash
YNAB_API="https://api.ynab.com/v1"

# Add a transaction
# POST \/budgets/\/transactions
# Body: {"transaction": {"account_id": "UUID", "date": "2026-03-06", "amount": -10000, "payee_name": "Coffee Shop", "category_id": "UUID", "approved": true}}

# Search transactions by payee
# GET \/budgets/\/transactions | jq filter by payee_name

# List categories
# GET \/budgets/\/categories
```

For the complete transfer guide, monthly spending calculation, and account ID management, see [references/api-guide.md](references/api-guide.md). For category naming examples, see [references/category-examples.md](references/category-examples.md).

## Agent Guidance

- Always categorize at transaction creation time -- searching past transactions for the same payee is the best way to find the right category.
- For transfers, always use `transfer_payee_id` from the destination account. Using `payee_name` is a common mistake that creates a regular expense instead.
- When calculating monthly spending, only count `amount < 0` and exclude transfers (`transfer_account_id != null`). Transfers are internal money movements, not expenses.
- Rate limit is ~200 requests/hour. Cache account and category data when doing bulk operations. **In caso di errore API (401, 429, 5xx), riprovare silenziosamente 2-3 volte con pausa di 10-15s prima di segnalare qualsiasi problema all'utente. MAI dichiarare che la chiave API è scaduta al primo errore 401 — è quasi sempre un rate limit temporaneo.**
- Never log or display full API keys in output.
- When running `daily-spending-report.sh`, the script outputs an "ANALYSIS DATA" section with raw metrics. Reinterpret this data in your own voice and style — give the user a brief, natural-language comment on their spending pace, highlight anything noteworthy, and mention the daily budget figure.

## Troubleshooting

- **401 Unauthorized**: ⚠️ **NON assumere subito che la chiave sia scaduta!** Spesso un 401 è causato da un rate limit temporaneo (l'API YNAB a volte restituisce 401 invece di 429 quando si supera il limite). **Prima azione:** aspettare 10-15 secondi e riprovare. Solo se il 401 persiste dopo 2-3 tentativi con pausa, allora la chiave potrebbe essere effettivamente scaduta. Mai dire all'utente di rigenerare il token come prima risposta.
- **404 Not Found**: Budget ID wrong -- check the YNAB URL
- **429 Too Many Requests**: Rate limit -- add delays between bulk calls. Aspettare 15-30 secondi prima di riprovare.
- **Transfer not linking**: Using `payee_name` instead of `transfer_payee_id`
- **Errori HTTP intermittenti**: In caso di qualsiasi errore API, riprovare almeno 2 volte con pausa di 10s prima di segnalare il problema all'utente.

API docs: https://api.ynab.com
