# Trade Templates Reference — 交易记录模板

## Standard Trade Entry (JSON)

### Futures Trade
```json
{
  "type": "futures",
  "date": "2026-05-20",
  "symbol": "IF2606",
  "direction": "long",
  "entry_price": 3850.0,
  "exit_price": 3900.0,
  "quantity": 2,
  "multiplier": 300,
  "entry_time": "09:35",
  "exit_time": "14:20",
  "fees": 45.60,
  "strategy": "trend_follow",
  "notes": "突破前高入场，尾盘止盈",
  "tags": ["股指", "日内", "趋势"],
  "open": false,
  "pnl": 29954.40
}
```

### Stock Trade
```json
{
  "type": "stock",
  "date": "2026-05-20",
  "symbol": "000001",
  "name": "平安银行",
  "direction": "long",
  "entry_price": 18.50,
  "exit_price": 19.20,
  "quantity": 1000,
  "entry_time": "10:00",
  "exit_time": "14:30",
  "fees": 15.00,
  "stamp_duty": 19.20,
  "strategy": "value_swing",
  "notes": "回踩均线买入，目标位到达止盈",
  "tags": ["银行", "A股"],
  "open": false,
  "pnl": 685.80
}
```

### Open Position (Unrealized)
```json
{
  "type": "futures",
  "date": "2026-05-20",
  "symbol": "IM2609",
  "direction": "short",
  "entry_price": 5650.0,
  "exit_price": null,
  "quantity": 1,
  "multiplier": 200,
  "entry_time": "13:45",
  "fees": 0,
  "strategy": "momentum",
  "stop_loss": 5720.0,
  "take_profit": 5500.0,
  "notes": "冲高回落开空，设好止损等夜盘",
  "tags": ["股指", "日内"],
  "open": true,
  "pnl": null
}
```

## Supported Strategies (tags)

| Tag | Description |
|:----|:------------|
| `趋势` / `trend` | Trend following |
| `日内` / `intraday` | Day trading |
| `波段` / `swing` | Swing trading |
| `套利` / `arbitrage` | Arbitrage / spread |
| `对冲` / `hedge` | Hedging |
| `突破` / `breakout` | Breakout strategy |
| `回踩` / `pullback` | Pullback entry |
| `网格` / `grid` | Grid trading |
| `量化` / `quant` | Quantitative / systematic |
| `手动` / `manual` | Manual / discretionary |

## Futures Contract Multipliers

| Exchange | Product Group | Multiplier |
|:---------|:--------------|:-----------|
| CFFEX | IF | 300 |
| CFFEX | IH | 300 |
| CFFEX | IC | 200 |
| CFFEX | IM | 200 |
| CFFEX | T/TF/TS/TL | 10000 |
| SHFE | CU/AL/ZN/PB | 5 (CU: 5) |
| SHFE | AU | 1000 |
| SHFE | AG | 15 |
| SHFE | RB/HC/SS | 10 |
| SHFE | RU | 10 |
| DCE | I | 100 |
| DCE | J | 100 |
| DCE | JM | 60 |
| DCE | C/A/M/Y/P | 10 |
| DCE | L/PP/V | 5 |
| ZCE | CF/SR | 5 |
| ZCE | MA/TA/RM | 10 |
| ZCE | FG/SA/UR | 20 |
| GFEX | SI | 5 |
| GFEX | LC | 1 |
| INE | SC | 1000 |
| INE | EC | 50 |
