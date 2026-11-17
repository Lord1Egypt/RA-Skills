---
name: stock-research
description: "Conduct evidence-first stock research with dated sources, data-quality gates, valuation, scenario analysis, falsifiable theses, and research-only recommendations. Use for single-stock analysis, peer comparisons, sector or theme baskets, thesis reviews, and buy/hold/watch/pass questions without trade execution. / 使用带日期的来源、数据质量门、估值、情景分析、可证伪论点和仅研究建议开展证据优先的股票研究；适用于个股分析、同业比较、行业或主题篮子、论点复盘，以及不执行交易的买入、持有、观察或放弃问题。"
license: Apache-2.0 OR MIT-0
metadata:
  version: "0.1.1"
---

# Evidence-First Stock Research / 证据优先股票研究

Build an auditable investment-research view from dated evidence to valuation and a bounded research stance. / 从带日期且可审计的证据出发，形成估值结论和边界明确的研究立场。

## Non-negotiable boundaries / 不可妥协的边界

- Never place or transmit a trade, broker payload, or standing instruction. / 不得下单或传输交易指令、券商载荷或持续性指令。
- Never request credentials, account identifiers, portfolio values, cookies, API keys, or tokens. / 不得索取凭证、账户标识、组合市值、Cookie、API Key 或 Token。
- Treat every output as research, not personalized investment advice. / 所有输出均为研究内容，而非个性化投资建议。
- Do not provide exact quantities, amounts, order types, limit prices, or executable allocations. / 不提供精确数量、金额、订单类型、限价或可执行仓位指令。
- Fail closed when evidence, freshness, valuation, or source provenance is insufficient. / 当证据、时效性、估值或来源溯源不足时，必须保守失败。
- State that data may be delayed, incomplete, or wrong and that capital can be lost. / 明确说明数据可能延迟、不完整或错误，投资可能损失本金。

Read [references/safety.md](references/safety.md) before producing a recommendation. / 输出建议前读取 [references/safety.md](references/safety.md)。

## Workflow / 工作流

### 1. Define the decision / 定义决策问题

Capture the symbols, market, research question, horizon, comparison set, and review date. / 记录标的、市场、研究问题、时间周期、比较集合和复盘日期。

Choose one mode: / 选择一种模式：

- `single_stock`: one company or security. / 单一公司或证券。
- `multi_compare`: normalized peer comparison. / 标准化同业比较。
- `sector_basket`: sector, theme, or factor basket. / 行业、主题或因子篮子。
- `thesis_review`: test what changed against a prior thesis. / 对照既有论点检验变化。

For a reusable offline checklist, run: / 如需可复用的离线清单，请运行：

```bash
python3 scripts/plan_stock_research.py \
  --symbols NVDA AMD AVGO \
  --market US \
  --mode multi_compare \
  --question "Compare AI compute exposure"
```

### 2. Build the evidence ledger / 建立证据账本

Prefer primary sources: regulator filings, issuer investor-relations material, audited statements, official transcripts, and official macro or industry data. / 优先使用监管文件、公司投资者关系材料、审计财报、官方电话会文本，以及官方宏观或行业数据。

For each material fact, capture publisher, URL, publication time, retrieval time, period covered, timezone where relevant, and whether the value is raw or derived. / 对每个重要事实记录发布方、URL、发布时间、获取时间、覆盖期间、相关时区，以及该数值属于原始数据还是派生数据。

Read [references/data-quality.md](references/data-quality.md) for source tiers, staleness gates, and conflict handling. / 来源分级、陈旧性门槛和冲突处理请读取 [references/data-quality.md](references/data-quality.md)。

### 3. Normalize the operating picture / 标准化经营图景

Use a consistent period and currency. Separate reported facts, consensus estimates, management guidance, and analyst assumptions. / 使用一致的期间和币种，并区分已披露事实、市场一致预期、管理层指引和分析假设。

At minimum, examine: / 至少检查：

- revenue, margins, earnings, free cash flow, returns on capital, and balance-sheet risk; / 收入、利润率、盈利、自由现金流、资本回报和资产负债表风险；
- segment economics, dilution, buybacks, dividends, and capital intensity; / 分部经济性、稀释、回购、分红和资本密集度；
- direct positive evidence, direct negative evidence, catalysts, and invalidation conditions. / 直接正面证据、直接负面证据、催化剂和失效条件。

### 4. Value the security / 对证券估值

Valuation is mandatory for a completed view. Use methods appropriate to the business, such as peer and historical multiples, DCF or reverse DCF, SOTP, asset-backed valuation, or a bear/base/bull scenario table. / 完整观点必须包含估值；应根据业务选择同业与历史倍数、DCF 或反向 DCF、SOTP、资产价值法，或熊市、基准、牛市情景表。

State assumptions, fair-value or scenario range, sensitivity drivers, and why each method fits. / 说明假设、公允价值或情景区间、敏感性驱动因素，以及各方法适用的原因。

Read [references/valuation.md](references/valuation.md) before finalizing the valuation section. / 完成估值部分前读取 [references/valuation.md](references/valuation.md)。

### 5. Form a falsifiable thesis / 形成可证伪论点

State the strongest supported thesis, the non-consensus element if one exists, the KPI or event that can disprove it, and a timebox for review. / 说明证据最充分的论点、存在时的非共识部分、可推翻它的 KPI 或事件，以及复盘时间限制。

If no defensible variant view exists, say so. / 如果不存在可辩护的差异化观点，应明确说明。

### 6. Issue a bounded research stance / 给出有边界的研究立场

Use one of: / 使用以下之一：

- `positive candidate`: evidence and valuation support deeper review. / 正面候选：证据和估值支持进一步研究。
- `hold thesis`: the existing thesis remains supported, without an execution instruction. / 持有论点：既有论点仍获支持，但不形成执行指令。
- `watch`: promising but blocked by missing evidence, freshness, or valuation. / 观察：具有潜力，但被证据、时效性或估值缺口阻断。
- `pass`: risk-reward or evidence quality is insufficient. / 放弃：风险收益或证据质量不足。
- `risk review`: direct negative evidence requires reassessment. / 风险复核：直接负面证据要求重新评估。

Include confidence, valuation range, trigger, invalidation condition, evidence grade, and unresolved gaps. / 包含置信度、估值区间、触发条件、失效条件、证据等级和未解决缺口。

### 7. Validate completion / 验证完成度

Represent the result as JSON and run the deterministic gate when useful: / 如适用，将结果表示为 JSON 并运行确定性门禁：

```bash
python3 scripts/validate_research_packet.py research.json --json
```

Do not call the research complete if the validator rejects missing valuation, undated sources, missing disclaimer, or execution fields. / 如果验证器发现缺失估值、来源未标日期、缺少免责声明或包含执行字段，不得声称研究已完成。

## Output contract / 输出契约

Return concise Markdown containing: / 返回包含以下内容的简洁 Markdown：

1. Research question and as-of time. / 研究问题与数据截至时间。
2. Evidence ledger with source quality and conflicts. / 包含来源质量和冲突的证据账本。
3. Operating and financial normalization. / 经营与财务标准化。
4. Valuation assumptions and scenario range. / 估值假设与情景区间。
5. Falsifiable thesis and disconfirming evidence. / 可证伪论点与反证。
6. Research stance, confidence, trigger, and invalidation. / 研究立场、置信度、触发条件和失效条件。
7. Risks, missing evidence, and next review date. / 风险、缺失证据和下次复盘日期。
8. Disclaimer: research only, not personalized investment advice; data may be delayed or wrong; loss of capital is possible. / 免责声明：仅供研究，并非个性化投资建议；数据可能延迟或错误；投资可能损失本金。

Read [references/workflows.md](references/workflows.md) for mode-specific checklists. / 各模式专用清单请读取 [references/workflows.md](references/workflows.md)。

## Version history / 版本历史

- `0.1.1` (2026-08-30): Added an explicit Apache-2.0 OR MIT-0 dual-license contract for consistent GitHub and ClawHub distribution. / 新增明确的 Apache-2.0 OR MIT-0 双许可证契约，使 GitHub 与 ClawHub 分发保持一致。
- `0.1.0` (2026-08-30): Initial public community edition with evidence, valuation, safety, and no-trade gates. / 首个公开社区版本，包含证据、估值、安全和禁止交易门禁。
