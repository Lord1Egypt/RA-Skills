## Description:

帮助 Shopee 卖家综合站点趋势、类目、竞店、热销商品与搜索需求，形成选品立项报告和决策建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and market researchers use this skill to assess major product opportunities and decide whether, what, and how to launch in a selected market.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Qinghu data requests may consume paid API credits.

Mitigation: Present the planned calls and obtain user consent before making them; report actual charges afterward.

Risk: API credentials and exported reports may contain sensitive business information.

Mitigation: Protect the Qinghu token and remove local report exports when they are no longer needed.

Risk: Third-party market data may differ from Shopee seller records.

Mitigation: Check important figures and assumptions against authoritative seller data before committing to a launch.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-decision)
- [Qinghu API key setup](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Structured Markdown report with links to exported tables for larger datasets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a recommendation, supporting market analysis, risks, and reported API usage costs.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
