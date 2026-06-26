# Portfolio & Transaction Guide

View your token holdings, portfolio history, and on-chain transaction activity to make informed trading decisions.

---

## Viewing Your Holdings

Check which tokens you currently hold:

```bash
node scripts/superhero-portfolio.mjs holdings
```

Check any address's holdings:

```bash
node scripts/superhero-portfolio.mjs holdings ak_...
```

Each holding shows:

- `token_name` / `token_symbol`
- `sale_address` — use this to swap back to AE
- `balance` — tokens held
- `balance_ae_value` — current AE value of that position
- `trending_score` — current momentum signal

---

## Portfolio Summary

Combined view of holdings + latest portfolio snapshot (AE/USD value, PnL):

```bash
node scripts/superhero-portfolio.mjs summary
```

---

## Portfolio Value History

See how your total portfolio value has changed over time:

```bash
node scripts/superhero-portfolio.mjs history
```

Returns all snapshots with:

- `total_value_ae` / `total_value_usd`
- `ae_balance` — liquid AE
- `tokens_value_ae` — value locked in token positions
- `total_pnl` — profit/loss object
- `tokens_pnl` — per-token PnL breakdown
- Period PnL summary (first vs latest snapshot)

---

## Viewing Transactions

### Your own trade history

```bash
node scripts/superhero-transactions.mjs mine
node scripts/superhero-transactions.mjs mine 50        # last 50 trades
```

### All trades on a specific token

Useful before buying — see if there is real buying pressure or just one whale:

```bash
node scripts/superhero-transactions.mjs token ct_...
node scripts/superhero-transactions.mjs token ct_... 30
```

### Trades by a specific account

Track a known trader or whale:

```bash
node scripts/superhero-transactions.mjs account ak_...
```

### All recent platform activity

Market-wide feed — see what is actively being traded right now:

```bash
node scripts/superhero-transactions.mjs all 20
```

### Activity: specific token + specific account

Check if a whale is accumulating a token you are watching:

```bash
node scripts/superhero-transactions.mjs activity ct_... ak_...
```

## Key Fields Reference

| Field              | Meaning                                         |
| ------------------ | ----------------------------------------------- |
| `sale_address`     | The bonding curve contract — use for buy/sell   |
| `balance_ae_value` | Current AE value of your position               |
| `total_pnl`        | Profit/loss since first purchase                |
| `trending_score`   | Momentum signal — higher = more buying pressure |
| `type`             | Transaction type: `buy` or `sell`               |
| `ae_amount`        | AE paid or received                             |
| `amount`           | Token quantity                                  |
