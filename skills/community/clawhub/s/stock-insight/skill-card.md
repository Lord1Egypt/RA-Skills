## Description:

股票深度分析Skill，遵循「起手式→总分总→可执行结论」三段式分析范式。输出专业感强、有人味、有惊喜的研判报告，检验标准：专业感、更懂用户、有惊喜、本质逻辑、高信噪比、事实准确。触发词：分析一下、研究、深度分析、怎么看、值不值得买、能不能涨、研判、洞察。

This skill is ready for commercial/non-commercial use.

## Publisher:

[karlinmoon](https://clawhub.ai/user/karlinmoon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to produce Chinese-language stock research reports that combine intent clarification, fundamentals, industry catalysts, capital flows, technical analysis, and actionable next steps. It is intended as analysis support and not as professional financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce concrete buy, sell, target-price, stop-loss, or position-size suggestions that could be mistaken for professional financial advice.

Mitigation: Treat outputs as analysis support only, preserve the investment-risk disclaimer, and verify decisions with current data and qualified advice before acting.

Risk: Stock analysis can be misleading if the request is not actually about a stock or if market and financial data are stale or missing.

Mitigation: Confirm the activation is stock-related, fetch current data during use, cite source timestamps, and mark missing data as unavailable rather than estimating it.

## Reference(s):

- [Analysis Examples](references/analysis-examples.md)
- [Industry Leading Indicators](references/industry-leading-indicators.md)
- [ClawHub Skill Page](https://clawhub.ai/karlinmoon/skills/stock-insight)
- [Publisher Profile](https://clawhub.ai/user/karlinmoon)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown stock research report in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current market data, source attribution, timestamps, explicit assumptions, and an investment-risk disclaimer.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
