# yf-cli Command Reference

Full flag reference for every `yf` subcommand. Load this file when you need precise flag names,
allowed values, or defaults beyond what `SKILL.md` covers.

---

## `yf quote`

```
yf quote [OPTIONS] TICKERS...
```

Accepts one or more space-separated tickers.

| Flag | Short | Values | Default |
|------|-------|--------|---------|
| `--output` | `-o` | `table` `json` `csv` | `table` |

**Examples**
```bash
yf quote AAPL
yf quote AAPL MSFT GOOGL
yf quote TSLA --output json
```

---

## `yf history`

```
yf history [OPTIONS] TICKER
```

| Flag | Short | Values | Default |
|------|-------|--------|---------|
| `--period` | `-p` | `1d` `5d` `1mo` `3mo` `6mo` `1y` `2y` `5y` `10y` `ytd` `max` | `1mo` |
| `--interval` | `-i` | `1m` `2m` `5m` `15m` `30m` `60m` `90m` `1h` `1d` `5d` `1wk` `1mo` `3mo` | `1d` |
| `--start` | | `YYYY-MM-DD` | — |
| `--end` | | `YYYY-MM-DD` | — |
| `--output` | `-o` | `table` `json` `csv` | `table` |

`--period` is ignored when `--start` / `--end` are given.

**Examples**
```bash
yf history AAPL
yf history AAPL --period 6mo --interval 1wk
yf history AAPL --start 2024-01-01 --end 2024-12-31
yf history AAPL --period 1y --output csv > aapl.csv
```

---

## `yf info`

```
yf info [OPTIONS] TICKER
```

| Flag | Short | Values | Default |
|------|-------|--------|---------|
| `--output` | `-o` | `table` `json` | `table` |

**Examples**
```bash
yf info AAPL
yf info TSLA --output json
```

---

## `yf financials`

```
yf financials [OPTIONS] TICKER
```

| Flag | Short | Values | Default |
|------|-------|--------|---------|
| `--type` | | `income` `balance` `cashflow` | `income` |
| `--freq` | | `annual` `quarterly` `ttm` | `annual` |
| `--output` | `-o` | `table` `json` `csv` | `table` |

`ttm` (trailing twelve months) is not available for the balance sheet.

**Examples**
```bash
yf financials AAPL
yf financials AAPL --type balance --freq quarterly
yf financials AAPL --type cashflow --freq ttm --output json
```

---

## `yf dividends`

```
yf dividends [OPTIONS] TICKER
```

| Flag | Short | Values | Default |
|------|-------|--------|---------|
| `--output` | `-o` | `table` `json` `csv` | `table` |

**Examples**
```bash
yf dividends AAPL
yf dividends KO --output csv
```

---

## `yf splits`

```
yf splits [OPTIONS] TICKER
```

| Flag | Short | Values | Default |
|------|-------|--------|---------|
| `--output` | `-o` | `table` `json` `csv` | `table` |

**Examples**
```bash
yf splits AAPL
yf splits TSLA --output json
```

---

## `yf actions`

```
yf actions [OPTIONS] TICKER
```

Combined view of dividends and splits in a single table.

| Flag | Short | Values | Default |
|------|-------|--------|---------|
| `--output` | `-o` | `table` `json` `csv` | `table` |

**Examples**
```bash
yf actions AAPL
yf actions MSFT --output csv
```

---

## `yf analyst`

```
yf analyst [OPTIONS] TICKER
```

| Flag | Short | Values | Default |
|------|-------|--------|---------|
| `--type` | | `targets` `recommendations` `upgrades` `estimates` | `targets` |
| `--output` | `-o` | `table` `json` `csv` | `table` |

| Type | Description |
|------|-------------|
| `targets` | Analyst price targets (low / mean / high) |
| `recommendations` | Ratings summary (Strong Buy / Buy / Hold / Sell) |
| `upgrades` | Recent upgrades and downgrades |
| `estimates` | EPS estimates |

**Examples**
```bash
yf analyst AAPL
yf analyst AAPL --type recommendations
yf analyst AAPL --type upgrades --output json
```

---

## `yf holders`

```
yf holders [OPTIONS] TICKER
```

| Flag | Short | Values | Default |
|------|-------|--------|---------|
| `--type` | | `major` `institutional` `mutualfund` `insider` | `major` |
| `--output` | `-o` | `table` `json` `csv` | `table` |

**Examples**
```bash
yf holders AAPL
yf holders MSFT --type institutional
yf holders TSLA --type insider --output csv
```

---

## `yf calendar`

```
yf calendar [OPTIONS] TICKER
```

| Flag | Short | Values | Default |
|------|-------|--------|---------|
| `--output` | `-o` | `table` `json` | `table` |

**Examples**
```bash
yf calendar AAPL
yf calendar MSFT --output json
```

---

## `yf options`

```
yf options [OPTIONS] TICKER
```

Omit `--expiry` to list available expiration dates first.

| Flag | Short | Values | Default |
|------|-------|--------|---------|
| `--expiry` | `-e` | `YYYY-MM-DD` | — (lists dates) |
| `--type` | | `both` `calls` `puts` | `both` |
| `--output` | `-o` | `table` `json` `csv` | `table` |

**Examples**
```bash
yf options AAPL                                  # list expiry dates
yf options AAPL --expiry 2025-06-20
yf options AAPL --expiry 2025-06-20 --type calls
yf options AAPL --expiry 2025-06-20 --output csv
```

---

## `yf search`

```
yf search [OPTIONS] QUERY
```

| Flag | Short | Values | Default |
|------|-------|--------|---------|
| `--type` | | `both` `quotes` `news` | `both` |
| `--limit` | `-n` | integer | `10` |
| `--output` | `-o` | `table` `json` | `table` |

**Examples**
```bash
yf search "electric vehicles"
yf search AAPL --type news --limit 5
yf search "semiconductor" --type quotes --output json
```

---

## `yf screen`

```
yf screen [OPTIONS]
```

| Flag | Short | Values | Default |
|------|-------|--------|---------|
| `--preset` | `-p` | see table below | — |
| `--limit` | `-n` | integer | `25` |
| `--list` | | flag | — |
| `--output` | `-o` | `table` `json` | `table` |

Use `--list` to print all available presets.

| Preset | Description |
|--------|-------------|
| `day-gainers` | Stocks with the highest % gain today |
| `day-losers` | Stocks with the biggest % drop today |
| `most-active` | Highest trading volume today |
| `most-shorted` | Most heavily shorted stocks |
| `aggressive-small-caps` | Small-cap stocks with aggressive growth |
| `small-cap-gainers` | Gaining small-cap stocks |
| `growth-tech` | Growth-oriented technology stocks |
| `undervalued-growth` | Undervalued stocks with growth potential |
| `undervalued-large-caps` | Large-cap stocks trading below value |
| `conservative-foreign-funds` | Conservative international mutual funds |
| `high-yield-bond` | High-yield bond funds |
| `portfolio-anchors` | Stable, foundational holdings |
| `solid-large-growth-funds` | Large-cap growth mutual funds |
| `solid-midcap-growth-funds` | Mid-cap growth mutual funds |
| `top-mutual-funds` | Top-performing mutual funds |
| `top-etfs-us` | Top US ETFs |
| `top-performing-etfs` | Best-performing ETFs |
| `technology-etfs` | Technology sector ETFs |
| `bond-etfs` | Bond ETFs |

**Examples**
```bash
yf screen --list
yf screen --preset day-gainers
yf screen --preset most-active --limit 10 --output json
```

---

## `yf market`

```
yf market [OPTIONS]
```

| Flag | Short | Values | Default |
|------|-------|--------|---------|
| `--sector` | `-s` | `basic-materials` `communication-services` `consumer-cyclical` `consumer-defensive` `energy` `financial-services` `healthcare` `industrials` `real-estate` `technology` `utilities` | — |
| `--top` | `-t` | `companies` `etfs` `mutual-funds` | `companies` |
| `--list` | | flag | — |
| `--output` | `-o` | `table` `json` | `table` |

**Examples**
```bash
yf market
yf market --list
yf market --sector technology
yf market --sector energy --top etfs
yf market --sector healthcare --output json
```

---

## `yf news`

```
yf news [OPTIONS] TICKER
```

| Flag | Short | Values | Default |
|------|-------|--------|---------|
| `--limit` | `-n` | integer | `10` |
| `--verbose` | `-v` | flag | off |
| `--output` | `-o` | `table` `json` | `table` |

`--verbose` adds full article summaries to the output.

**Examples**
```bash
yf news AAPL
yf news NVDA --limit 5
yf news TSLA --verbose
yf news MSFT --output json
```

---

## Global Flag

| Flag | Applies to | Description |
|------|-----------|-------------|
| `--no-color` | all commands | Disable ANSI colour codes in output |

```bash
yf quote AAPL --no-color
```

---

## JSON Response Schemas

### `yf quote --output json`

Returns an array, one object per ticker.

```json
[
  {
    "symbol": "AAPL",
    "currency": "USD",
    "last_price": 269.39,
    "previous_close": 271.5,
    "open": 271.44,
    "day_high": 272.8,
    "day_low": 269.35,
    "volume": null,
    "market_cap": 3959400939044.0,
    "fifty_day_average": 260.51,
    "two_hundred_day_average": 252.44,
    "change": -2.115,
    "change_pct": -0.78
  }
]
```

### `yf financials --output json`

Returns an object keyed by fiscal period date. Each key maps to a flat object of line-item names → values (floats or null).

```json
{
  "2025-09-30": {
    "TotalRevenue": 416161000000.0,
    "GrossProfit": 195201000000.0,
    "OperatingIncome": 133050000000.0,
    "EBITDA": 144748000000.0,
    "NetIncome": 112010000000.0,
    "DilutedEPS": 7.46,
    "BasicEPS": 7.49
  }
}
```

### `yf options --expiry DATE --output json`

Returns an object with `"calls"` and/or `"puts"` arrays (depending on `--type`). Each element represents one contract.

```json
{
  "calls": [
    {
      "contractSymbol": "AAPL260422C00190000",
      "lastTradeDate": "2026-04-21 13:39:26+00:00",
      "strike": 190.0,
      "lastPrice": 81.17,
      "bid": 79.95,
      "ask": 83.2,
      "change": -1.25,
      "percentChange": -1.52,
      "volume": 4.0,
      "openInterest": 1,
      "impliedVolatility": 3.44,
      "inTheMoney": true,
      "contractSize": "REGULAR",
      "currency": "USD"
    }
  ]
}
```

When `--expiry` is omitted, the output is a plain table of available expiration dates (not JSON).
