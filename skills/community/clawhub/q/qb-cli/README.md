# quickbooks-online-cli

QuickBooks Online CLI tool for AI agents and humans. Manage your books from the terminal — talks directly to Intuit's QuickBooks API with no third-party proxy.

164 commands across 29 groups: AR, AP, chart of accounts, banking, reporting, imports, reconciliation, and month-end workflows.

## Prerequisites

- **Docker** and **Docker Compose**
- A [QuickBooks developer account](https://developer.intuit.com) with an app created
- Your **Client ID** and **Client Secret** from the Keys & OAuth section
- `http://localhost:8844/callback` added as a Redirect URI in your app settings

## Install

```bash
git clone https://github.com/claw4business/quickbooks-online-cli.git ~/skills/qb-cli
cd ~/skills/qb-cli
cp .env.example .env
# Edit .env with your Client ID and Client Secret
docker compose build
```

## Authenticate

```bash
# Get the OAuth URL
~/skills/qb-cli/run.sh auth login --print-url

# Open the URL in a browser, authorize, then paste the callback URL back:
~/skills/qb-cli/run.sh auth login --callback-url "http://localhost:8844/callback?code=...&realmId=..."
```

## Quick Start

```bash
# Check auth status
~/skills/qb-cli/run.sh auth status

# List customers
~/skills/qb-cli/run.sh customer list -o table

# Create an invoice
~/skills/qb-cli/run.sh invoice create --customer-id 123 --amount 500 --due-date 2026-04-01

# Run a P&L report
~/skills/qb-cli/run.sh report profit-and-loss --start-date 2026-01-01 --end-date 2026-01-31 -o table
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `QB_CLIENT_ID` | Yes | Your QuickBooks app Client ID |
| `QB_CLIENT_SECRET` | Yes | Your QuickBooks app Client Secret |
| `QB_ENVIRONMENT` | No | `sandbox` (default) or `production` |

## Command Groups (29)

`auth` `config` `company` `customer` `invoice` `payment` `estimate` `credit-memo` `sales-receipt` `refund-receipt` `vendor` `bill` `bill-payment` `vendor-credit` `purchase-order` `account` `item` `expense` `journal` `deposit` `transfer` `report` `import` `reconcile` `workflow` `batch` `preferences` `tax` `attachment`

See [SKILL.md](SKILL.md) for full command reference and agent integration guide.

## License

MIT
