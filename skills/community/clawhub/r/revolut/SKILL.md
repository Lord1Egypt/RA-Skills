---
name: revolut
description: "Revolut web automation via Playwright: login/logout, list accounts, fetch transactions, and download Invest statements (year-end holdings, realised P&L, costs and charges)."
summary: "Revolut banking automation: login, accounts, transactions, portfolio, statements."
version: 1.4.0
homepage: "https://github.com/odrobnik/revolut-skill"
metadata:
  openclaw:
    emoji: "💳"
    requires:
      bins: ["python3", "playwright"]
      python: ["playwright"]
---

# Revolut Banking Automation

Fetch current account balances, investment portfolio holdings, and transactions for all wallet currencies and depots in JSON format. Uses Playwright to automate Revolut web banking.

**Entry point:** `{baseDir}/scripts/revolut.py`

## Setup

See [SETUP.md](SETUP.md) for prerequisites and setup instructions.

## Commands

```bash
python3 {baseDir}/scripts/revolut.py --user oliver login
python3 {baseDir}/scripts/revolut.py --user oliver accounts
python3 {baseDir}/scripts/revolut.py --user oliver transactions --from YYYY-MM-DD --until YYYY-MM-DD
python3 {baseDir}/scripts/revolut.py --user sylvia portfolio
python3 {baseDir}/scripts/revolut.py --user oliver invest-transactions --from YYYY-MM-DD --until YYYY-MM-DD
python3 {baseDir}/scripts/revolut.py --user oliver invest-statements --year YYYY [--type all|account|pnl|costs] [--format pdf|csv] [--dir DIR]
```

## Updating Banker (Full Refresh)

To fully synchronize Revolut data into the `banker` archive:

```bash
# 1. Login (needs approval via Revolut App)
python3 {baseDir}/scripts/revolut.py --user oliver login

# 2. Export accounts + portfolios
python3 {baseDir}/scripts/revolut.py --user oliver --out /tmp/rev_accounts.json accounts
python3 {baseDir}/scripts/revolut.py --user oliver --out /tmp/rev_portfolio.json portfolio

# 3. Export transactions (separated by wallet and invest depot)
# Find Wallet IDs from the accounts JSON (e.g. EUR wallet, USD wallet)
python3 {baseDir}/scripts/revolut.py --user oliver --out /tmp/rev_tx_eur.json transactions --account <EUR-WALLET-ID> --from 2025-01-01 --until 2026-12-31
python3 {baseDir}/scripts/revolut.py --user oliver --out /tmp/rev_tx_usd.json transactions --account <USD-WALLET-ID> --from 2025-01-01 --until 2026-12-31
python3 {baseDir}/scripts/revolut.py --user oliver --out /tmp/rev_invest_tx.json invest-transactions --from 2025-01-01 --until 2026-12-31

# 4. Import into banker
# Accounts and Wallet transactions
python3 ~/Developer/Skills/banker/scripts/banker.py import --bank oliver@revolut /tmp/rev_accounts.json /tmp/rev_tx_eur.json /tmp/rev_tx_usd.json

# Invest portfolio & transactions (must specify --account revolut_gia)
python3 ~/Developer/Skills/banker/scripts/banker.py import --bank oliver@revolut --account revolut_gia /tmp/rev_portfolio.json
python3 ~/Developer/Skills/banker/scripts/banker.py import --bank oliver@revolut --account revolut_gia --kind transactions /tmp/rev_invest_tx.json

# 5. Logout
python3 {baseDir}/scripts/revolut.py --user oliver logout
```

## Invest exports: what the rows mean (since 1.4.0)

`invest-transactions` exports every completed item of the brokerage feed, not only trades:

| kind | meaning | amount sign |
|---|---|---|
| `buy` / `sell` | securities trades (quantity, price, total incl. fees) | cash paid / received |
| `cash_top_up` | money moved from a Revolut pocket into the brokerage account | + |
| `withdrawal` | money moved out of the brokerage account | − |
| `dividend` | net dividend credited to the brokerage cash (`gross` and `tax` kept alongside) | + |
| other | any new feed type, exported with its raw type as `kind` | by side |

Every row carries the feed item `id`, which banker uses for de-duplication. The brokerage cash balance can therefore be reconstructed as `top-ups − withdrawals − buys + sells + dividends`, and `portfolio` now also returns a `cash` list (one entry per currency, with `availableToInvest` and `unsettled`); `accounts` puts the main cash balance into the depot entry's `balances.booked`.

Re-importing after the upgrade: older chunks have no ids, so banker would keep both copies of a trade. Export the whole depot history once (`--from` the depot's opening date), import it, and delete the older id-less chunks with `banker.py files` / `banker.py delete`.

## Invest statements (year-end depot, P&L)

`invest-statements` downloads the brokerage documents Revolut offers in the Invest web app (Documents), for a calendar year (`--year`) or any range (`--from`/`--until`; a future end date is clamped to today):

| `--type` | document | formats |
|---|---|---|
| `account` | account statement: starting/ending value, **portfolio breakdown at the period end** (symbol, ISIN, quantity, price, value), cash, all transactions | pdf, csv |
| `pnl` | realised profit and loss: every sale with acquisition/sale date, cost basis, proceeds, gross P&L and fees, in USD and EUR with the FX rates | pdf, csv |
| `costs` | costs and charges report (ex-post cost disclosure) | pdf only |

Default is `--type all --format pdf`. Files go to `--dir` (workspace or `/tmp`; default `/tmp/openclaw/revolut/statements`) as `revolut_<user>_<kind>_<from>_<until>.<ext>`; stdout (or `--out`) gets a JSON list of the written files. Revolut generates each document on request, which takes a few seconds per file.

```bash
# Year-end documents for the tax return
python3 {baseDir}/scripts/revolut.py --user oliver invest-statements --year 2025 --dir ~/clawd/revolut/statements
```

## Recommended Flow

```
login → accounts → transactions → portfolio → logout
```

Always call `logout` after completing all operations to delete the stored browser session.

## Notes
- Per-user state stored in `{workspace}/revolut/` (deleted by `logout`).
- Output paths (`--out`) are sandboxed to workspace or `/tmp`.
- No `.env` file loading — credentials in config.json only.
