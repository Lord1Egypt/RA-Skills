---
name: exchange-rate
version: 1.0.0
description: >
  汇率换算 — 查询实时汇率、历史汇率、汇率趋势。数据源为欧洲央行 (ECB)。
  触发词: 汇率, 换算, exchange rate, convert currency, 多少钱,
  美元, 欧元, 日元, 英镑, USD, EUR, JPY, GBP,
  或任何 "[金额] [货币A] 转/换/to [货币B]" 格式的输入。
---

# exchange-rate — Currency Exchange Rate Skill

Query real-time and historical exchange rates via the Frankfurter API (ECB data source).

## Quick Start
1. No API key needed.
2. Run `bun scripts/exchange.ts --help` in this skill directory.
3. Pick the matching command from `references/command-map.md`.

## Workflow
1. Parse user intent — identify source currency, target currency, amount, and date (if any).
2. Select the right command: `convert`, `latest`, `history`, or `currencies`.
3. Run the script and return the result.
4. When the user provides a natural language query like "100 美元换人民币", use the `convert` command with `--amount 100 --from USD --to CNY`.

## Commands
- Full command mapping: `references/command-map.md`

## Common Currency Aliases
When the user uses Chinese names, map them:
- 美元/美金 → USD
- 人民币/元 → CNY
- 欧元 → EUR
- 英镑 → GBP
- 日元/日币 → JPY
- 韩元/韩币 → KRW
- 港币/港元 → HKD
- 新加坡元/新币 → SGD
- 澳元/澳币 → AUD
- 加元/加币 → CAD
- 泰铢 → THB
- 瑞士法郎/瑞郎 → CHF

## Notes
- This skill is script-first and does not run an MCP server.
- Data source is ECB (European Central Bank), updated once per working day.
- Supports 30 major currencies.
- No API key required.
