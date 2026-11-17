## Description:

Provides a Chinese-language A-share stock analysis workflow that classifies a stock as value, growth, breakout, or concept-driven, then produces a ten-book panoramic analysis with ratings, price ranges, and position guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[w5208111111](https://clawhub.ai/user/w5208111111)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial-analysis agents use this skill to produce Chinese-language A-share stock analyses from a stock name or code. When a cutoff date is supplied, the skill frames the output as a timeline-constrained backtest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce buy, watch, or avoid ratings with price ranges and position percentages that may be mistaken for professional financial advice.

Mitigation: Treat outputs as informational analysis, keep the disclaimer visible, and verify decisions with qualified financial advice and independent market data.

Risk: Current analysis and backtests can be misleading if market, financial, news, or cutoff-date data is stale or outside the stated timeline.

Mitigation: Validate all quoted data against reliable sources and, in backtest mode, use only information that was available on or before the supplied cutoff date.

## Reference(s):

- [Ten-Book Analysis Framework](references/tenbook-analysis.md)
- [Type-C Breakout Framework](references/type-c-framework.md)
- [Standard Output Template](references/output-template.md)
- [Tencent Market Quote API](https://qt.gtimg.cn/q=sz002602)
- [Tencent 52-Week K-Line API](https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=CODE,day,START,END,300,,)
- [Sina Financial Indicators](https://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/CODE/ctrl/YEAR/displaytype/4.phtml)
- [Zhiliaocaibao PE Percentile](https://www.zhiliaocaibao.com/gz_pe/CODE_名称_9/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown analysis with tables, ratings, price ranges, position percentages, and disclaimers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; may include current-analysis or backtest framing depending on the user's prompt.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
