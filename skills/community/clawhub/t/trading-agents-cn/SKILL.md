---
name: trading-agents-cn
description: |-
  基于 LLM 的 A 股多智能体交易分析框架，支持批量选股对比、回测信号生成和因子研究，自带 OpenAI 兼容 API 适配器模板。
license: Proprietary. See LICENSE.txt in project root.
compatibility: Designed for Doramagic-host ecosystem (Claude Code / openclaw / Cursor). Requires Python 3.12+ with uv package manager.
metadata:
  version: "v6.1"
  blueprint_id: "finance-bp-099"
  compiled_at: "2026-04-22T13:00:44.877519+00:00"
  capability_markets: "cn-astock"
  capability_activities: "backtesting, factor-research"
  sop_version: "crystal-compilation-v6.1"
---
# A 股多智能体 (trading-agents-cn)

> 基于 LLM 的 A 股多智能体交易分析框架，支持批量选股对比、回测信号生成和因子研究，自带 OpenAI 兼容 API 适配器模板。

## Pipeline

`data_collection -> data_storage -> factor_computation -> target_selection -> trading_execution -> visualization`

## Top Use Cases (29 total)

### LLM Adapter Template for OpenAI-Compatible Providers (`UC-101`)
Users need a template to create custom LLM adapters for OpenAI-compatible API providers to integrate with TradingAgents framework
**Triggers**: llm adapter, openai compatible, custom provider

### Batch Stock Analysis with Comparison Reports (`UC-102`)
Investors need to analyze multiple stocks simultaneously and generate comparison reports for portfolio selection and sector analysis
**Triggers**: batch analysis, multiple stocks, comparison report

### Custom Stock Analysis with Focus Selection (`UC-108`)
Investors need customized stock analysis with selectable focus areas like technical, fundamental, risk assessment, or sector comparison
**Triggers**: custom analysis, analysis focus, personalized

For all **29** use cases, see [references/USE_CASES.md](references/USE_CASES.md).

**Execute trigger**: `When user intent matches intent_router.uc_entries[].positive_terms AND user uses action verb (run/execute/跑/执行/backtest/fetch/collect)`

## What I'll Ask You

- Target market: A-share (default), HK, or crypto? (US stocks in ZVT are half-baked — stockus_nasdaq_AAPL exists but coverage is thin)
- Data source / provider: eastmoney (free, no account), joinquant (account+paid), baostock (free, good history), akshare, or qmt (broker)?
- Strategy type: MACD golden-cross, MA crossover, volume breakout, fundamental screen, or custom factor?
- Time range: start_timestamp and end_timestamp for backtest period
- Target entity IDs: specific stocks (stock_sh_600000) or index components (SZ1000)?

## Semantic Locks (Fatal)

| ID | Rule | On Violation |
|---|---|---|
| `SL-01` | Execute sell orders before buy orders in every trading cycle | halt |
| `SL-02` | Trading signals MUST use next-bar execution (no look-ahead) | halt |
| `SL-03` | Entity IDs MUST follow format entity_type_exchange_code | halt |
| `SL-04` | DataFrame index MUST be MultiIndex (entity_id, timestamp) | halt |
| `SL-05` | TradingSignal MUST have EXACTLY ONE of: position_pct, order_money, order_amount | halt |
| `SL-06` | filter_result column semantics: True=BUY, False=SELL, None/NaN=NO ACTION | halt |
| `SL-07` | Transformer MUST run BEFORE Accumulator in factor pipeline | halt |
| `SL-08` | MACD parameters locked: fast=12, slow=26, signal=9 | halt |

Full lock definitions: [references/LOCKS.md](references/LOCKS.md)

## Top Anti-Patterns (25 total)

- **`AP-ZVT-183`**: 除权因子为 inf/NaN 时直接参与乘法导致复权静默失败
- **`AP-ZVT-179`**: 第三方数据接口超限后异常被吞噬，数据静默缺失
- **`AP-ZVT-183B`**: HFQ（后复权）与 QFQ（前复权）K 线表使用错误导致因子计算漂移

All 25 anti-patterns: [references/ANTI_PATTERNS.md](references/ANTI_PATTERNS.md)

## Evidence Quality Notice

> [QUALITY NOTICE] This crystal was compiled from blueprint finance-bp-099. Evidence verify ratio = 32.5% and audit fail total = 33. Generated results may have uncaptured requirement gaps. Verify critical decisions against source files (LATEST.yaml / LATEST.jsonl).

## Reference Files

| File | Contents | When to Load |
|---|---|---|
| [references/seed.yaml](references/seed.yaml) | V6+ 全量权威 (source-of-truth) | 有行为/决策争议时必读 |
| [references/ANTI_PATTERNS.md](references/ANTI_PATTERNS.md) | 25 条跨项目反模式 | 开始实现前 |
| [references/WISDOM.md](references/WISDOM.md) | 跨项目精华借鉴 | 架构决策时 |
| [references/CONSTRAINTS.md](references/CONSTRAINTS.md) | domain + fatal 约束 | 规则冲突时 |
| [references/USE_CASES.md](references/USE_CASES.md) | 全量 KUC-* 业务场景 | 需要完整示例时 |
| [references/LOCKS.md](references/LOCKS.md) | SL-* + preconditions + hints | 生成回测/交易代码前 |
| [references/COMPONENTS.md](references/COMPONENTS.md) | AST 组件地图（按 module 拆分）| 查 API 时 |

---

*Compiled by Doramagic crystal-compilation-v6.1 from `finance-bp-099` blueprint at 2026-04-22T13:00:44.877519+00:00.*
*See [human_summary.md](human_summary.md) for non-technical overview.*
