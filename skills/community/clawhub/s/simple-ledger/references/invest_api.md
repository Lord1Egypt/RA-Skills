# Investment Tracking — Command Reference

> ⚠️ **Network:** All `--allow-network` flags require user confirmation. Without `--allow-network`, commands use last-set prices from `investments.csv`.

## File Location

Default: `~/.openclaw/workspace/data/ledger/investments.csv`

## Buy / Sell

### Buy (auto-lookup code by name)

```bash
invest.py --buy "<证券名称>" auto <数量> <单价> <日期> --allow-network
```

Example:
```bash
invest.py --buy "有色金属ETF南方" auto 3100 2.07 2026-01-10 --allow-network
```

Behavior:
1. Queries Sina/Eastmoney for the security code
2. If unique match → shows trade summary, requires Y/N to confirm
3. If multiple candidates → lists options, asks user to pick
4. If no match → prompts for manual code

### Buy (manual code)

```bash
invest.py --buy "<名称>" <代码> <数量> <单价> <日期>
```

Example:
```bash
invest.py --buy "沪深300ETF" 510050 100 3.50 2026-01-15
```

### Sell

```bash
invest.py --sell "<名称>" <代码> <数量> <单价> <日期>
```

Example:
```bash
invest.py --sell "沪深300ETF" 510050 500 4.00 2026-03-01
```

## Price & Cost

### Update current price (manual, no network)

```bash
invest.py --price <代码> <价格>
```

Example:
```bash
invest.py --price 601138 81.58
```

### Update cost basis

```bash
invest.py --cost <代码> <新成本>
```

Example:
```bash
invest.py --cost 601138 66.589
```

## Quotes & Refresh

### Single-quote lookup

```bash
invest.py --quote <代码> --allow-network
```

Example:
```bash
invest.py --quote 601138 --allow-network
```

### Refresh all holdings

```bash
invest.py --refresh --allow-network
```

## Portfolio & Reports

### Portfolio (offline, last-set prices)

```bash
invest.py --portfolio
```

### Portfolio with live quotes

```bash
invest.py --portfolio --auto-refresh
```

### Single-holding P&L

```bash
invest.py --return <代码>
```

Example:
```bash
invest.py --return 510050
```

### Total P&L summary

```bash
invest.py --summary
```

With live quotes:

```bash
invest.py --summary --auto-refresh
```

## History

### List all transactions

```bash
invest.py --list
```

## Global Options

| Flag | Description |
|------|-------------|
| `--allow-network` | Permit one-off network call (code lookup or quote) |
| `--auto-refresh` | Auto-fetch live quotes for portfolio/summary |
| `--csv <file>` | Use a non-default `investments.csv` path |
| `--no-input` | Skip Y/N confirmation (for batch scripts only) |

## Auto-refresh Mode

Create `~/.openclaw/workspace/data/ledger/.env` with:

```
AUTO_REFRESH=1
```

After this, `--portfolio` and `--summary` always fetch live quotes (no need to add `--auto-refresh`).

To disable: delete the `.env` file or set `AUTO_REFRESH=0`.

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `network blocked` | `--allow-network` missing | Add the flag (one-off) or enable auto-refresh |
| `code not found` | Security name has no Sina/Eastmoney match | Provide code manually with `--buy <名称> <代码>` |
| `insufficient holdings` | Sell quantity > current holding | Check portfolio with `--portfolio` |
| `csv not found` | First run, no investments.csv | Use `--buy` to create the file |

## Data Format

`investments.csv` columns:

```
date,action,code,name,quantity,price,account,note
```

Where:
- `date` — YYYY-MM-DD
- `action` — `buy` or `sell`
- `code` — 6-digit code (510050, 601138, etc.)
- `name` — security name (used for display)
- `quantity` — shares (decimal allowed for funds)
- `price` — per-share price
- `account` — payment account (same as ledger accounts)
- `note` — optional memo

The script also maintains a sidecar state (in CSV comment lines) tracking last-set current prices per code.

## Worked Example

```bash
# 1. First buy (uses network to find code)
invest.py --buy "贵州茅台" auto 10 1600.00 2026-06-01 --allow-network
# → Shows trade summary, prompts Y/N → after Y, appends to investments.csv

# 2. Set current price manually (no network)
invest.py --price 600519 1685.50

# 3. Check portfolio
invest.py --portfolio
# Shows: 贵州茅台 (600519) | 10 shares @ cost 1600.00 | current 1685.50 | +5.34%

# 4. Or auto-refresh for live price
invest.py --portfolio --auto-refresh

# 5. Partial sell
invest.py --sell "贵州茅台" 600519 5 1700.00 2026-06-15
# → Shows gain, prompts Y/N

# 6. Summary
invest.py --summary
```

See `invest_guide.md` for workflow philosophy and net-cost method explanation.
