## Description:

12维股票智能分析评分模型，基于行业、头部玩家、市场环境、管理团队、市值规模、主营业务、收入、利润、分红、回购、机构持股、大股东增减持12个维度对股票进行综合评分。

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankxpj](https://clawhub.ai/user/frankxpj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to score a stock across 12 weighted business and market dimensions, then generate a Markdown or JSON report for comparison, portfolio review, and investment-decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated stock scores and buy, hold, or exit ratings could be mistaken for financial advice.

Mitigation: Treat outputs as a user-driven scoring aid, verify market and company data independently, and make investment decisions outside the skill.

Risk: Broad stock-analysis requests may trigger the skill even when the user expects current market data.

Mitigation: Confirm the requested scope and require current, independently sourced market data before relying on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frankxpj/skills/stock-smart-analyse)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown report or JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include weighted dimension scores, an overall rating, strengths, focus areas, and a timestamp.]

## Skill Version(s):

1.0.0 (source: release evidence and skill version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
