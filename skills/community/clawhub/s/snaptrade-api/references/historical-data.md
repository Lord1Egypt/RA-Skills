# Historical Data (Activities / Transactions)

Activities are the historical record of all transactions that resulted in a
position change — buys, sells, dividends, contributions, withdrawals, etc.

**Activities vs Orders:**
- **Orders** — includes pending and cancelled orders, granular timestamps, short history
- **Activities** — completed position-changing transactions only, years of history

For most historical analysis, use activities.

---

## Fetch Activities

Paginated. Default page size: 1000. Returns in reverse chronological order.

```python
response = snaptrade.transactions_and_reporting.get_activities(
    user_id=user_id,
    user_secret=user_secret,
    accounts=account_id,       # single account_id string
    start_date="2024-01-01",   # optional, ISO date string YYYY-MM-DD
    end_date="2024-12-31",     # optional
)
activities = response.body
```

### Multiple accounts

```python
response = snaptrade.transactions_and_reporting.get_activities(
    user_id=user_id,
    user_secret=user_secret,
    accounts=",".join([account_id_1, account_id_2]),
)
```

---

## Activity Object Fields

| Field | Description |
|---|---|
| `type` | Transaction type: `BUY`, `SELL`, `DIVIDEND`, `CONTRIBUTION`, `WITHDRAWAL`, etc. |
| `amount` | Cash impact. Positive = cash gained. Negative = cash spent. |
| `units` | Position impact. Positive = shares gained (BUY). Negative = shares lost (SELL). |
| `price` | Price per share at time of transaction. |
| `symbol` | Universal symbol object (ticker, exchange, currency). |
| `currency` | Currency of the transaction. |
| `trade_date` | ISO-8601 datetime of the transaction. |
| `description` | Human-readable description from the brokerage. |

**Interpreting amount/units:**
- BUY: `units > 0`, `amount < 0` (gained shares, spent cash)
- SELL: `units < 0`, `amount > 0` (lost shares, gained cash)
- DIVIDEND: `units = 0`, `amount > 0` (cash received, no position change)

---

## History Depth

History depth varies by brokerage. Examples:
- Schwab: up to 4 years
- Most others: full account history since inception

Check the SnapTrade Broker Support Matrix for specifics on each brokerage.

---

## Pagination

If an account has a very large number of transactions, the initial sync may
take time. If no activities are returned immediately after connecting, retry
after a short delay — the initial indexing may still be in progress.
