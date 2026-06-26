---
name: shadow-trading-dashboard
description: Manage Steven's A-share shadow trading dashboard. Triggers on: (1) "影子盘看板", "交易看板", "持仓状况", (2) placing or updating a simulated trade (buy/sell/止损/止盈), (3) updating positions or equity data, (4) reviewing trade history or P&L. Reads and writes to the shadow trading system under trade/.
---

# Shadow Trading Dashboard

## Dashboard Location
`trade/dashboard/index.html` — 影子盘看板主文件，双击用浏览器打开

## Core Data Files

| File | Purpose |
|------|---------|
| `trade/dashboard/index.html` | Dashboard HTML |
| `trade/dashboard_data/metrics.json` | KPI metrics |
| `trade/dashboard_data/equity_curve.json` | Equity curve |
| `trade/data/positions.json` | Current positions |
| `trade/data/orders.jsonl` | Order log |
| `trade/trades.csv` | Open positions CSV |
| `trade/closed_positions.csv` | Closed positions CSV |
| `trade/trade_history.md` | Human-readable trade history |

## Data Schema

### positions.json
```json
{
  "symbol": "300274",
  "name": "阳光电源",
  "quantity": 300,
  "cost": 163.16,
  "current_price": 166.59,
  "stop_loss": 160.00,
  "tags": ["储能","龙头"],
  "entry_reason": "储能龙头ROE29%，回调支撑买入"
}
```

### metrics.json
```json
{
  "current_equity": 1001029.00,
  "position_market_value": 49977.00,
  "cash": 951037.32,
  "unrealized_pnl": 1029.00,
  "realized_pnl": 0.0,
  "total_return_pct": 0.103,
  "trade_count": 1,
  "win_count": 0,
  "loss_count": 0,
  "max_drawdown": 0.0
}
```

## Standard Workflows

### Opening the Dashboard
```bash
open ~/.openclaw/workspace/trade/dashboard/index.html
```

### After Any Trade (Buy/Sell/Stop)
1. Update `trade/data/positions.json`
2. Append to `trade/data/orders.jsonl`
3. Update `trade/trades.csv` and `trade/closed_positions.csv`
4. Update `trade/dashboard_data/metrics.json`
5. Update `trade/dashboard_data/equity_curve.json`
6. Rebuild `trade/dashboard/index.html` (update DATA object + equity curve)
7. Update `trade/trade_history.md`
8. Run `open trade/dashboard/index.html`

### Building the Dashboard HTML
The dashboard is a self-contained HTML with an embedded DATA object. Key fields to update:
- `current_equity`, `cash`, `position_value`, `unrealized_pnl`, `realized_pnl`
- `positions[]` array (name, symbol, quantity, cost, current_price, stop_loss, tags)
- `trade_history[]` array (date, time, symbol, name, action, direction, price, quantity, amount, fee, pnl, tags)
- `closed_positions[]` for closed trades
- `equity_curve[]` for the curve

### Fees
- A股模拟手续费：0.03% 单边（买卖各收一次）
- Fee = price × quantity × 0.0003

### Equity Calculation
- `current_equity` = cash + Σ(position market value)
- Market value = current_price × quantity

## Dashboard Update Checklist
After any trade, ALL of these must be updated:
- [ ] `trade/data/positions.json`
- [ ] `trade/data/orders.jsonl` (append new order)
- [ ] `trade/trades.csv` (open positions)
- [ ] `trade/closed_positions.csv` (closed positions)
- [ ] `trade/dashboard_data/metrics.json`
- [ ] `trade/dashboard_data/equity_curve.json`
- [ ] `trade/dashboard/index.html` (DATA object + equity_curve)
- [ ] `trade/trade_history.md`
