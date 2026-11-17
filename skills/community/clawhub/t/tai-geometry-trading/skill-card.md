## Description:

融合东方智慧和几何数学的交易分析系统，使用几何结构、多周期 MACD 风洞共振、缩量短线、基本面、情绪和 AI 预测分析来输出股票走势和交易评分报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[saitoshen](https://clawhub.ai/user/saitoshen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run Chinese-language stock technical analysis, optional LLM-assisted scoring, and trading-signal report generation for questions about stock trends, buy or sell timing, technical analysis, and stock ratings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives actionable trading scores and buy/sell language that may be mistaken for personalized investment advice.

Mitigation: Treat outputs as general information and require independent financial review before trading decisions.

Risk: API keys may be configured directly in scripts/config.py.

Mitigation: Use environment variables or a private secrets file instead of committing or sharing real API keys.

Risk: The full analysis path may send market-analysis prompts to external LLM providers.

Mitigation: Review provider settings and data-sharing expectations before enabling LLM-backed analysis.

Risk: Some auxiliary scores can be defaults or placeholders when supporting data or API configuration is unavailable.

Mitigation: Verify data availability and treat default auxiliary scores as incomplete analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/saitoshen/skills/tai-geometry-trading)
- [太几何交易参考文档](references/technical_guide.md)
- [股票基本面分析参考](references/fundamental_analysis.md)
- [Tushare](https://tushare.pro)
- [MiniMax](https://www.minimax.chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text reports with stock scores, signal summaries, risk notes, recommendations, Python code examples, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch live market data and may call configured external LLM providers when API keys are supplied.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
