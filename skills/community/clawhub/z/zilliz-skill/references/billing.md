
## Prerequisites

1. CLI installed and logged in via OAuth (see setup skill).
2. Billing features require OAuth login -- API Key mode may not have access.

## Commands Reference

### Query Usage

```bash
# Last N days
zilliz billing usage --last 7d

# Current month
zilliz billing usage --month this

# Last month
zilliz billing usage --month last

# Specific month
zilliz billing usage --month 2026-01

# Custom date range
zilliz billing usage --start 2026-01-01 --end 2026-01-31
```

### List Invoices

```bash
# List all invoices (paginated)
zilliz billing invoices

# Fetch all pages
zilliz billing invoices --all

# Paginate manually
zilliz billing invoices --page-size 10 --page 1
```

### View Invoice Details

```bash
zilliz billing invoices --invoice-id inv-xxxxxxxxxxxx
```

### Bind a Credit Card

```bash
zilliz billing bind-card \
  --card-number <credit-card-number> \
  --exp-month <expiration-month> \
  --exp-year <expiration-year> \
  --cvc <card-verification-code>
```

## Guidance

- Billing commands require OAuth login, not API Key authentication.
- When the user asks about costs or spending, use `billing usage` with an appropriate time range.
- The `bind-card` command handles sensitive card data -- always instruct the user to run it in their own terminal, never inside Claude Code.
