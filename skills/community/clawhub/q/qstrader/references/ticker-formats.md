# Форматы тикеров

## Брокерские тикеры (для ордеров)

Используются в `Place_Order`, `Close_an_open_deal`, `Deals`.
Полный список: `instrument.json` (16,709 инструментов).

| Актив | Брокерский тикер | Yahoo Finance |
|---|---|---|
| S&P 500 | US500 | ^GSPC |
| Dow Jones | US30 | ^DJI |
| NASDAQ 100 | US100 | ^NDX |
| Золото | XAUUSD | GC=F |
| Серебро | XAGUSD | SI=F |
| EUR/USD | EURUSD | EURUSD=X |
| GBP/USD | GBPUSD | GBPUSD=X |
| USD/JPY | USDJPY | USDJPY=X |
| Tesla | TSLA | TSLA |
| VIX / Волатильность | VXX | ^VIX |

## Yahoo Finance тикеры (для аналитики)

Используются в `get_technical_analysis`, `predict_future_price_lstm`,
`get_options_data`, `get_company_fundamentals`, новости.

### Индексы
- `^GSPC` — S&P 500
- `^DJI` — Dow Jones
- `^IXIC` — NASDAQ Composite
- `^NDX` — NASDAQ 100
- `^RUT` — Russell 2000

### Товары
- `GC=F` — Золото (Gold Futures)
- `SI=F` — Серебро
- `CL=F` — Нефть (Crude Oil)
- `NG=F` — Газ

### Форекс
- `EURUSD=X` — EUR/USD
- `GBPUSD=X` — GBP/USD
- `USDJPY=X` — USD/JPY

### Акции
- `TSLA` — Tesla
- `AAPL` — Apple
- `NVDA` — NVIDIA

## LSTM формат дат

```
YYYY-MM-DD-HH-MM
```

Примеры:
- `2025-04-27-00-00` — 27 апреля 2025, 00:00
- `2026-03-28-16-00` — 28 марта 2026, 16:00

### Расчёт дат для LSTM
- **start_date**: текущая дата − 330 дней (≈11 месяцев)
- **end_date**: текущая дата + 1 день

## Как найти брокерский тикер

```python
import json
with open("instrument.json") as f:
    instruments = json.load(f)

# Поиск по описанию
matches = [i for i in instruments if "S&P" in i.get("description", "")]
for m in matches:
    print(m["ticker"], "-", m["description"])
```
