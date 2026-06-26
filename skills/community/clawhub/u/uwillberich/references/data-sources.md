# Data Sources

Use primary and official sources first when the conclusion depends on policy, rates, or geopolitics.

## Official And Primary Sources

| Source | Use | Notes |
|---|---|---|
| `pbc.gov.cn` | `LPR`, PBOC guidance, domestic policy timing | Use exact release dates and times |
| `federalreserve.gov` | FOMC statements and projections | Use official statement pages for exact wording |
| `bankofengland.co.uk` | BOE policy decisions | Useful when global rates affect risk appetite |
| `snb.ch` | SNB policy decisions | Secondary global rates input |
| `apnews.com` / `reuters.com` | Geopolitics, oil, fast macro news | Use for timely cross-market context |

## Market Data Endpoints In This Skill

## Source Priority

| Layer | Primary | Secondary | Benchmark Command |
|---|---|---|---|
| Index and sector tape | Eastmoney public endpoints | none in this skill | `python3 scripts/benchmark_sources.py --skip-mx` |
| Liquid stock quotes | Tencent quote snapshot | none in this skill | `python3 scripts/benchmark_sources.py --skip-mx` |
| High-attention event intake | Google News / BBC / NYT / WSJ RSS | direct web verification | `python3 scripts/benchmark_sources.py --skip-mx` |
| Financial news search | `mx_toolkit.py news-search` | public RSS + primary websites | `python3 scripts/benchmark_sources.py` |
| Stock screening | `mx_toolkit.py stock-screen` | static watchlists | `python3 scripts/benchmark_sources.py` |
| Structured security data | `mx_toolkit.py query` | public quote snapshot for a quick check | `python3 scripts/benchmark_sources.py` |

### Tencent Quote Snapshot

- Endpoint: `https://qt.gtimg.cn/q=...`
- Use: liquid stock watchlists
- Encoding: `GBK`
- Key parsed fields:
  - name
  - code
  - price
  - prior close
  - open
  - high
  - low
  - absolute change
  - percent change
  - amount
  - timestamp

### Eastmoney Index Snapshot

- Endpoint: `https://push2.eastmoney.com/api/qt/ulist.np/get`
- Use: main index levels and simple breadth
- Default symbols:
  - `1.000001` Shanghai Composite
  - `0.399001` Shenzhen Component
  - `0.399006` ChiNext
  - `1.000300` CSI 300
  - `1.000688` STAR 50
  - `0.899050` Beijing 50

### Eastmoney Sector Breadth

- Endpoint: `https://push2.eastmoney.com/api/qt/clist/get`
- Use: strongest and weakest sectors on the day
- The skill defaults to concept-board ranking with the common Eastmoney parameters already set in the script.

### MX News Search

- Endpoint: `https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search`
- Use: timely finance news search with stronger source coverage than public RSS
- Entry point in this skill:
  - `python3 scripts/mx_toolkit.py news-search --query '立讯精密 最新资讯'`
  - `python3 scripts/mx_toolkit.py preset --name preopen_policy`

### MX Stock Screen

- Endpoint: `https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen`
- Use: natural-language board and stock screening
- Entry point in this skill:
  - `python3 scripts/mx_toolkit.py stock-screen --keyword 'A股 光模块概念股'`
  - `python3 scripts/mx_toolkit.py preset --name board_optical_module`

### MX Structured Data Query

- Endpoint: `https://mkapi2.dfcfs.com/finskillshub/api/claw/query`
- Use: entity-level structured data such as latest price, market cap, and time-series tables
- Entry point in this skill:
  - `python3 scripts/mx_toolkit.py query --tool-query '浪潮信息 最新价 总市值 收盘价'`
  - `python3 scripts/mx_toolkit.py preset --name validate_inspur`

## Practical Notes

- These public endpoints may throttle or change.
- Use scripts for fast snapshots, not for blindly trusting a single source.
- Use `benchmark_sources.py` before assigning a source as the primary feed for a live session.
- If the user asks for the latest or today’s view, verify the unstable facts live before drawing conclusions.
