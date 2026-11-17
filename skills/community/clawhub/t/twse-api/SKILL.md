---
name: twse-api
description: Query Taiwan Stock Exchange (TWSE) open data via the official OpenAPI (https://openapi.twse.com.tw) — daily stock prices/OHLC, P/E ratio, dividend yield, P/B, market index (TAIEX) history, company profiles and financial statements, monthly revenue, margin trading, block trades, ESG disclosures, warrants, broker data, and the trading calendar. Use this skill whenever the user asks about Taiwan stocks, 台股, 上市公司, TWSE/證交所 data, Taiwanese stock quotes or fundamentals, TAIEX/加權指數, or wants to fetch/analyze any Taiwan listed-company data, even if they don't mention the API by name.
---

# TWSE OpenAPI (Taiwan Stock Exchange 臺灣證券交易所)

Official open-data API of the Taiwan Stock Exchange. Free, no API key, no registration.

- **Base URL**: `https://openapi.twse.com.tw/v1`
- **Method**: all endpoints are plain `GET`, **no parameters at all** (no query string, no path params)
- **Response**: always a JSON array of flat objects; **every value is a string** (numbers included)
- Full endpoint catalog: 143 endpoints across 7 categories (see [Endpoint catalog](#endpoint-catalog) below)
- Swagger spec: `https://openapi.twse.com.tw/v1/swagger.json` (docs UI: https://openapi.twse.com.tw/)

## Critical conventions (read before calling)

1. **No server-side filtering.** Each endpoint returns the *entire* dataset (typically the latest trading day's snapshot, or a historical series). To get data for one stock, fetch the whole array and filter client-side by stock code (`Code` or `公司代號`). Responses range from a few rows to ~30,000 rows (insider-transfer tables), so filter with a script rather than dumping raw output into context.

2. **Two field-naming styles.** Endpoints under `/exchangeReport`, `/indicesReport`, `/announcement`, `/block`, `/fund`, `/holidaySchedule` etc. mostly use **English** JSON keys (`Code`, `Name`, `ClosingPrice`…). Endpoints under `/opendata` (the `t187ap*` datasets) use **Traditional Chinese** JSON keys (`公司代號`, `公司名稱`, `營業收入-當月營收`…). The reference files list the exact keys per endpoint — use them verbatim; do not guess or translate key names.

3. **ROC (Minguo 民國) dates.** Most `Date`/`出表日期` values look like `1150706` = ROC year 115, July 6 = **2026-07-06** (Gregorian year = ROC year + 1911). Some fields (e.g. company founding date `成立日期`) use Gregorian `YYYYMMDD` instead — check the magnitude: 7 digits starting with `1` is ROC, 8 digits starting with `19`/`20` is Gregorian.

4. **Snapshot data, not historical query.** Most endpoints only expose the latest period: `STOCK_DAY_ALL` = latest trading day, `FMSRFK_ALL` = current month's aggregate (one row per stock), `FMNPTK_ALL` = current year's aggregate. There is no way to request an arbitrary past date through this API. True historical series exist only where noted (e.g. `/indicesReport/MI_5MINS_HIST` for TAIEX daily history).

5. **Number parsing.** Numeric strings may contain commas (`"1,030,726,137"`), be empty, or be `"-"`/`"－"` for N/A. Strip commas and handle blanks before converting.

6. **Data scope is TWSE listed (上市) securities.** OTC/TPEx (上櫃) securities are served by a different API (`https://www.tpex.org.tw/openapi/`), not this one. Endpoints suffixed `_L` = listed companies (上市), `_P`/`_X` = public non-listed companies (公開發行).

## Quick start

```bash
# Daily OHLC for all listed stocks, filter for TSMC (2330)
curl -s https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL |
  python3 -c "import json,sys; print([r for r in json.load(sys.stdin) if r['Code']=='2330'])"
```

```python
import json, urllib.request

BASE = "https://openapi.twse.com.tw/v1"

def twse(path):
    with urllib.request.urlopen(BASE + path) as r:
        return json.load(r)

# P/E, dividend yield, P/B for one stock
row = next(r for r in twse("/exchangeReport/BWIBBU_ALL") if r["Code"] == "2330")
# {'Code': '2330', 'Name': '台積電', 'PEratio': '...', 'DividendYield': '...', 'PBratio': '...'}

# Company profile (Chinese keys!)
tsmc = next(r for r in twse("/opendata/t187ap03_L") if r["公司代號"] == "2330")
```

## Task → endpoint cheat sheet

| Task | Endpoint |
|---|---|
| Today's OHLC/volume, all stocks | `/exchangeReport/STOCK_DAY_ALL` |
| P/E, dividend yield, P/B | `/exchangeReport/BWIBBU_ALL` |
| Closing price + monthly average | `/exchangeReport/STOCK_DAY_AVG_ALL` |
| Per-stock current-month / current-year aggregate | `/exchangeReport/FMSRFK_ALL` / `FMNPTK_ALL` |
| TAIEX index history (daily OHLC) | `/indicesReport/MI_5MINS_HIST` |
| Whole-market daily volume/value | `/exchangeReport/FMTQIK` |
| Company basic profile | `/opendata/t187ap03_L` |
| Monthly revenue, all companies | `/opendata/t187ap05_L` |
| Income statement (general industry) | `/opendata/t187ap06_L_ci` |
| Balance sheet (general industry) | `/opendata/t187ap07_L_ci` |
| Dividend distributions | `/opendata/t187ap45_L` |
| Material news / announcements | `/opendata/t187ap04_L` |
| Ex-dividend calendar | `/exchangeReport/TWT48U_ALL` |
| Margin trading balances | `/exchangeReport/MI_MARGN` |
| Trading holidays / market calendar | `/holidaySchedule/holidaySchedule` |
| TWSE news | `/news/newsList` |

## Endpoint catalog

Read the reference file for the category you need — each lists every endpoint with its exact response keys (Chinese originals kept as comments):

| Reference file | Category (原分類) | Endpoints | Contents |
|---|---|---|---|
| [references/securities-trading.md](references/securities-trading.md) | 證券交易 | 36 | Daily quotes, valuation ratios, market stats, margin/block/day trading, attention & disposition stocks, market calendar |
| [references/corporate-governance.md](references/corporate-governance.md) | 公司治理 | 56 | Company profiles, insider/director holdings, board data, material news, dividends, shareholder meetings, 21 ESG datasets |
| [references/financial-statements.md](references/financial-statements.md) | 財務報表 | 30 | Monthly revenue, income statements & balance sheets by industry format, profitability summaries |
| [references/indices.md](references/indices.md) | 指數 | 5 | TAIEX, Taiwan 50, Formosa Index histories |
| [references/warrants.md](references/warrants.md) | 權證 | 3 | Warrant issuance and trading stats |
| [references/brokers.md](references/brokers.md) | 券商資料 | 9 | Securities firm directories, personnel, monthly financials |
| [references/misc.md](references/misc.md) | 其他 | 4 | TWSE news/events, government bonds, funds |
