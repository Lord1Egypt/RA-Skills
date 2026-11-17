## Description:

天枢股票分析系统 uses Tencent Finance quote data and a seven-theory framework to produce informational stock diagnostic reports with scores, ratings, and action suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horizoncove](https://clawhub.ai/user/horizoncove)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch live stock quote data and generate an informational stock diagnosis, including multi-factor scores, short- and long-term ratings, and suggested actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact instructs agents to disable TLS checks while fetching live financial data, which could allow quote data or resulting advice to be tampered with.

Mitigation: Keep TLS certificate validation enabled and remove the TLS-disabling instructions before routine financial-analysis use.

Risk: The skill produces ratings and operation suggestions for stocks.

Mitigation: Treat outputs as informational only and require independent financial review before making trading decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horizoncove/skills/tianshu-stock)
- [Tencent Finance quote endpoint example](https://qt.gtimg.cn/q=sh603127)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown diagnostic report with quote fields, theory-by-theory analysis, scores, ratings, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live market data from Tencent Finance when network access is available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
