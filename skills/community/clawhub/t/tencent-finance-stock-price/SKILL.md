---
name: tencent-finance-stock-price
description: Query real-time stock data using Tencent Finance API. Supports Chinese A-shares, Hong Kong, and US stocks with market cap, TTM PE, PB, volume, turnover, total shares, and 52-week range. No API key required. Universal tool — accepts any valid stock code.
---

# Tencent Finance Stock Price

Universal stock quote tool via Tencent Finance API (qt.gtimg.cn). Accepts any valid stock code. Auto-detects market (A/HK/US) via index [0] and adapts field parsing per market.

## Quick Start

```bash
# Compact mode (default): price, change%, market cap
uv run ~/.openclaw/skills/tencent-finance-stock-price/scripts/query_stock.py sh688256 hk02026 usAAPL

# Detail mode: PE(TTM), PB, volume, turnover, total shares, turnover rate, 52-week range
uv run ~/.openclaw/skills/tencent-finance-stock-price/scripts/query_stock.py --detail 688256 02026
```

## Examples

```bash
# A-shares — Kweichow Moutai, CATL, Cambricon
uv run query_stock.py 600519 300750 688256

# HK stocks — Pony.ai, Tencent
uv run query_stock.py 02026 00700

# US stocks — Apple
uv run query_stock.py usAAPL

# Indices
uv run query_stock.py sh000001 hkHSI usINX
```

## Code Format

- A-share: `sh688256` `sz300750` (raw 6-digit: `688256` `300750`)
- HK: `hk02026` `hk00700` (raw 5-digit: `02026` `00700`)
- US: `usAAPL` `usWOLF` (must use prefix)

## Sample Output (Compact)

```
Name                     Price      Change   Chg%        Mkt Cap
------------------------------------------------------------------
Cambricon              1316.88      39.01 🟢  3.05%     8274B CNY
Pony.ai-W                70.35      0.450 🟢  0.64%      30.5B HKD
Apple                   294.80       2.12 🟢  0.72%       4.3T USD
```

## Sample Output (Detail `-d`)

```
============================================================
  Tencent (00700)  HK
============================================================
  Price: 462.600 HKD
  Change: 🟢 5.400  (1.18%)
  Mkt Cap: 4.2T HKD  |  Float Cap: 4.2T HKD
  PE(TTM): 16.94  |  PB: 2.58
  Volume: 26.62M sh  |  Turnover: 12.26B HKD
  Total Shares: 9.12B sh  |  Lot Size: 100 sh
  52w High: 683.000  |  52w Low: 454.000
```

## API Field Mapping

**A-shares**: Price [3], Change [31]/Chg% [32], Volume [6], Turnover [37]×10K CNY, PE(TTM) [39], PB [46], Total/Float MktCap [45]/[44] 亿 CNY, Total/Float Shares [73]/[72], 52w H/L [47]/[48]

**HK**: Price [3], Change [31]/Chg% [32], Volume [6] shares, Turnover [37] HKD, PE(TTM) [39], PB [43], Total/Float MktCap [45]/[44] 亿 HKD, Total/Float Shares [69]/[70], Lot Size [60], 52w H/L [48]/[49]

**US**: Price [3], Change [31]/Chg% [32], Volume [6] shares, Turnover [37] USD, PE(TTM) [38], PB [43], Total/Float MktCap [45]/[44] 亿 USD, Total/Float Shares [62]/[63], 52w H/L [48]/[49]

- PE(TTM): trailing-twelve-month P/E. Negative for loss-making companies (e.g. -29.26).
- A-share volume: API sometimes returns 手 (lots), sometimes shares. Auto-detected via turnover rate cross-validation.
