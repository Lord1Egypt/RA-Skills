---
name: "taiwan-fund"
description: "Query Taiwan mutual fund NAV, performance, holdings via cnyes/MoneyDJ. Compare funds, auto currency conversion."
---

# Taiwan Fund Skill 🇹🇼💰

查詢台灣境內/境外基金淨值、績效、持股明細，**外幣計價基金自動匯率換算**、**多檔基金比較**、**跟指數/ETF 對比績效**。

## Data Sources

| 來源 | 用途 | URL/Pattern |
|------|------|-------------|
| **鉅亨網 (cnyes)** `__NEXT_DATA__` | 境內基金 NAV + 績效（1M/3M/1Y）+ 排行（主要來源） | `https://invest.cnyes.com/funds/detail/{name}/{code}/overview` |
| **TDCC OpenAPI** | 境外基金 NAV 備援（ISIN 查詢，快取 12h） | `https://openapi-t.tdcc.com.tw/v1/opendata/3-4` |
| **Yahoo Finance** | 指數/ETF 歷史績效回測 | `https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=5y&interval=1d` |
| **open.er-api.com** | 匯率（30-min 快取） | `https://open.er-api.com/v6/latest/USD` |

### 資料源優先順序

```
查詢基金 → cnyes __NEXT_DATA__ (境內基金, 最完整)
         → TDCC 3-4 (境外基金, 有 ISIN 才有)
         → 回報無資料
```

## Commands

```bash
# 查基金淨值（外幣自動換算台幣）
python3 scripts/twfund.py nav A09022

# 比較多檔基金
python3 scripts/twfund.py compare A36004 A09022
python3 scripts/twfund.py compare A36004 --with 00981A.TW ^TWII
python3 scripts/twfund.py compare --all --with 0050.TW 006208.TW VOO

# 快取 TDCC 境外基金資料（第一次會下載 8MB，之後快取 12h）
python3 scripts/twfund.py tdcc-init

# 查匯率
python3 scripts/twfund.py rate USD
python3 scripts/twfund.py rate EUR

# 搜尋基金
python3 scripts/twfund.py search "摩根美國增長"

# 列出追蹤清單
python3 scripts/twfund.py watchlist

# 產生鉅亨 URL
python3 scripts/twfund.py cnyes A36004
```

## Fund Codes Format

追蹤清單 `fund_codes.json`，支援 `currency`、`benchmark`、`isin` 欄位：

```json
{
  "A09022": {
    "name": "統一台灣動力基金-A類型",
    "category": "股票-台灣",
    "currency": "TWD",
    "benchmark": "^TWII"
  },
  "LU1309713268": {
    "name": "聯博-美國收益基金IA(穩定月配)級別美元",
    "category": "債券-全球",
    "currency": "USD",
    "isin": "LU1309713268",
    "benchmark": "^GSPC"
  }
}
```

| 欄位 | 說明 | 預設值 |
|------|------|--------|
| `name` | 基金全名 | 必填 |
| `category` | 分類標籤（顯示用） | 選填 |
| `currency` | 計價幣別 | `"TWD"` |
| `isin` | ISIN 代碼（境外基金用，走 TDCC 查淨值） | 選填 |
| `benchmark` | 比較基準指數的 Yahoo Symbol | 選填 |

**境內基金**用鉅亨網代碼（Axxxxx）當 key，會從 cnyes 抓 NAV + 績效。
**境外基金**用 ISIN 當 key，cnyes 查不到會自動降級到 TDCC 取 NAV（需先跑 `tdcc-init` 快取）。

### Benchmark 支援的常見代碼

| 名稱 | Yahoo Symbol | 別名 |
|------|-------------|------|
| 台股加權指數 | `^TWII` | 加權指數、大盤 |
| 櫃買指數 | `^TWO` | 櫃買 |
| S&P 500 | `^GSPC` | sp500、標普500 |
| 那斯達克 | `^IXIC` | nasdaq、那斯達克 |
| 元大台灣50 | `0050.TW` | 0050、台灣50 |
| 富邦台50 | `006208.TW` | 006208、富邦台50 |

### 支援幣別

TWD、USD、EUR、JPY、GBP、AUD、ZAR、CNY、SGD、HKD、KRW、NZD、CHF、SEK

## Usage Flow

### 1️⃣ 查單一基金

```bash
python3 scripts/twfund.py nav A36004
```
```
📡 安聯台灣科技基金  (A36004)
   📊 最新淨值: NT$790.69  (2026/06/11)  [cnyes]
   📈 績效: 1M: +2.36% | 3M: +58.47% | 1Y: +263.27%
   🏆 同組排名: 3M 前9% | 1Y 前1%
   規模: 2672.5億 | 管理費: 1.6% | ★5
```

境外基金（有 `isin`）則走 TDCC：
```
📡 聯博-美國收益基金IA  (LU1309713268)
   📊 最新淨值: $10.60  (20260611)  [TDCC]
   💱 台幣等值: NT$335.06  (匯率 1 美元 = NT$31.61)
```

### 2️⃣ 比較多檔 + 看指數/ETF

```bash
python3 scripts/twfund.py compare A36004 A09022 --with 0050.TW ^TWII
```

輸出包含各基金的淨值、績效、超額報酬、規模、排名，以及底部的績效一覽表。

### 3️⃣ 外幣基金匯率換算

`currency` 設為非 TWD 時自動抓匯率 + 轉台幣。

### 4️⃣ Benchmark 自動對比

`benchmark` 有設的話，compare 會自動算超額報酬。

## TDCC 快取說明

- `tdcc-init` 下載集保境外基金開放資料（~8MB），建立 ISIN → NAV 索引
- 快取在 `~/.openclaw/cache/taiwan-fund/tdcc_nav.json`，有效 12 小時
- 只需執行一次，之後自動讀取快取
- 第一次下載約需 10~30 秒（8MB JSON）

## 注意

- 境內基金用鉅亨網 cnyes 爬 `__NEXT_DATA__`，最完整（含績效 + 排名）
- 境外基金若 cnyes 查不到 + 有 ISIN，會降級到 TDCC（只有 NAV，無績效）
- 匯率快取 30 分鐘，TDCC 快取 12 小時
- 指數/ETF 績效從 Yahoo Finance 拉 5 年 daily data 回算
- `fund_codes.json` 使用者自行維護
