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
- When calculating monthly spending, only count `amount < 0` and consider excluding non-discretionary categories (taxes, transfers).
- Rate limit is ~200 requests/hour. Cache account and category data when doing bulk operations.
- Never log or display full API keys in output.
- When running `daily-spending-report.sh`, the script outputs an "ANALYSIS DATA" section with raw metrics. Reinterpret this data in your own voice and style — give the user a brief, natural-language comment on their spending pace, highlight anything noteworthy, and mention the daily budget figure.

## Troubleshooting

- **401 Unauthorized**: Token invalid or expired -- regenerate at https://app.ynab.com/settings/developer
- **404 Not Found**: Budget ID wrong -- check the YNAB URL
- **429 Too Many Requests**: Rate limit -- add delays between bulk calls
- **Transfer not linking**: Using `payee_name` instead of `transfer_payee_id`

API docs: https://api.ynab.com