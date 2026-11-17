---
name: quant-strategy-interpreter
display_name: StrategyLens 量化策略精读包
description: 量化交易与期货策略解读助手。触发词：量化策略、回测、期货策略、双均线、海龟交易法则、均值回归、布林带、动量突破、跨期套利、配对交易、统计套利、策略参数、文献解读、英文论文策略复现。把英文量化/期货文献中的策略思想转化为中文解读 + 可运行回测模板（Python/pandas）+ 参数说明 + 文献出处，并调用「数据查询 MCP」取真实行情回测。
version: 1.0.0
author: StrategyLens
license: MIT
tags:
  - quant
  - futures
  - backtest
  - options
  - risk
  - mcp
  - finance
  - python
homepage: https://clawhub.ai/skill/strategylens
agent_created: true
---

# 量化策略解读助手（Quant Strategy Interpreter）

## 概述
帮助用户把英文量化交易 / 期货文献中的策略思想，转化成**可直接上手**的中文材料：
策略解读 + 可运行回测模板 + 参数说明 + 文献出处，并可调用配套「数据查询 MCP」获取真实历史行情做回测验证。

## 何时使用（触发场景）
当用户提到：量化策略、回测、期货策略、双均线、海龟交易法则（Turtle）、均值回归、布林带（Bollinger）、动量突破、跨期套利、配对交易、统计套利、策略参数、文献解读、英文论文/书籍策略复现。

## 工作流程
1. **明确标的与周期**：问清品种（如沪深300期货、黄金、BTC、AAPL）与数据源（yahoo / akshare / ccxt）。
2. **取数（调用 MCP）**：用 `get_price_history(symbol, source, start, end)` 拉历史 K 线（字段：date/open/high/low/close/volume）。
3. **策略解读**：从 `references/strategies.md`（通用 6 策略模板）与 `references/systematic_main.md`（文献深做章节）调取对应策略的中文解读、回测模板、参数说明。
4. **回测**：把数据代入 `scripts/backtest_template.py` 的对应函数，输出信号序列与策略收益（position × returns 近似）。
5. **参数建议**：按品种波动特性给参数区间，提示过拟合风险。
6. **合规收尾**：每次必须附风险免责声明；任何解读均不复制原文，只引用出处。

## 策略库索引（详见 references/strategies.md）
| 策略 | 英文 | 适用市场 | 关键参数 |
|---|---|---|---|
| 双均线交叉 | MA Crossover | 趋势市（股/期/币） | short/long 周期 |
| 海龟交易法则 | Turtle Trading | 突破/趋势（期货为主） | 唐奇安通道 N、ATR |
| 布林带均值回归 | Bollinger Reversion | 震荡市 | 周期/标准差倍数 k |
| 动量突破 | Momentum | 中期动量品种 | 回看窗口 |
| 跨期套利 | Calendar Spread | 商品期货近远月 | 价差 z-score |
| 配对交易 | Pair Trading | 高相关品种对 | 价差 z-score/半衰期 |

## 数据接入示例（MCP）
```
# 在 WorkBuddy 中配置好 quant-data-mcp 后，直接要求：
# "用 get_price_history 取 AU0（akshare 国内黄金期货）2025 全年日线，跑双均线回测"
```

## 注意事项（红线）
- **不提供交易建议、不下单、不对接任何券商交易 API**。
- **不复制受版权保护的英文原文**；只做中文重写解读 + 注明文献出处（书名/作者/年份/章节）。
- 所有回测皆为历史模拟，存在过拟合与未来函数风险，输出须标注「仅供研究，非投资建议」。
- 期货/杠杆品种风险极高，务必提示用户理解保证金与爆仓机制。

## 文献引用规范
格式：`作者(年份)《书名》章节X — 用自己话概括的观点`。不得大段摘录原文。

## 文献深做章节索引（详见 references/systematic_main.md）
| 原版文献 | 对应模块 | 配套脚本 |
|---|---|---|
| Carver(2015)《Systematic Trading》 | 波动率目标化仓位、风险预算 | scripts/vol_target_position.py |
| Carver(2017)《Smart Portfolios》 | 组合层资金分配、风险平价 | scripts/risk_parity.py |
| Clenow(2015)《Stocks on the Move》 | 股票动量策略 | scripts/momentum_equity.py |
| Tomasini & Jaekle(2009)《Trading Systems》 | 系统开发流程、防过拟合 | scripts/backtest_guardrails.py |
| Teweles & Jones(2008)《The Futures Game》 | 期货机制、套保基础 | （见章节文字） |
| Aronson(2006)《Evidence-Based TA》 | 统计显著性、样本外检验 | scripts/backtest_guardrails.py |
| Sinclair(2020)《Positional Option Trading》 | 期权头寸、Greeks、波动率 | scripts/option_greeks.py |
| Hilpisch(2015)《Derivatives Analytics with Python》 | 期权定价、Greeks | scripts/option_greeks.py |
| Grant(2004)《Trading Risk》 | 交易风控框架、限额 | （见章节文字） |
| Danielsson(2011)《Financial Risk Forecasting》 | 波动预测、VaR/ES | scripts/risk_forecast.py |
| Aldridge(2013)《HFT: A Practical Guide》 | 高频策略分类、微观结构 | references/hft_microstructure.md |
| MacKenzie(2021)《Trading at the Speed of Light》 | HFT 生态与制度 | references/hft_microstructure.md |
| Lehalle & Laruelle(2018)《Market Microstructure in Practice》 | 订单簿、执行优化 | references/hft_microstructure.md |
| Dacorogna et al.(2001)《Intro to High-Frequency Finance》 | 高频数据计量 | references/hft_microstructure.md |
| Stefanica(2011)《Primer for Math of FE》 | 量化数学基础 | references/quant_foundations.md |
| Regenstein(2018)《Reproducible Finance with R》 | 可重复研究 | references/quant_foundations.md |
| Chincarini & Kim(2009)《Quantitative Equity PM》 | 因子模型、组合优化 | references/quant_foundations.md + scripts/equity_portfolio.py |
| Wilmott(2008)《FAQ in Quant Finance》 | 概念速查 | references/quant_foundations.md |
| MacLean et al.(2011)《Kelly Capital Growth》 | 凯利/半凯利仓位 | references/quant_foundations.md + scripts/kelly_position.py |
| Kuznetsov(2006)《Complete Guide to Capital Markets》 | 市场结构图谱 | references/quant_foundations.md |

完整 20 本文献的索引地图见 `references/literature.md`。
