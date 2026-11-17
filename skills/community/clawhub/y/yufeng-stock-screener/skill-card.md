## Description:

A股智能量化选股助手（禹锋量化 · 专业版）用于在用户询问A股选股、股票推荐、短线机会、强势股、涨停股分析、个股技术分析、主力资金流向或择时建议时调用量化筛选能力。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsy0303](https://clawhub.ai/user/wsy0303)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request A-share stock screening, individual stock analysis, sector fund-flow summaries, token status checks, and short-term timing scores through the publisher's quantitative stock API. The skill is focused on A-share market analysis and explicitly excludes Hong Kong stocks, U.S. stocks, funds, futures, bonds, and wealth-management products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill sends paid API tokens to an external service over insecure HTTP.

Mitigation: Review before installing; avoid sending sensitive trading or account information unless the endpoint is changed to HTTPS, and rotate any token previously sent over the HTTP endpoint.

Risk: The security evidence says the installer can persist the API token in shell startup files.

Mitigation: Prefer passing the token per command or using a proper secret store instead of writing it to ~/.bashrc.

Risk: The skill produces short-term stock-screening and timing guidance that may affect investment decisions.

Mitigation: Treat outputs as informational only, review results independently, and preserve the skill's risk reminder that results do not constitute investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wsy0303/skills/yufeng-stock-screener)
- [Publisher profile](https://clawhub.ai/user/wsy0303)
- [Yufeng Quant API service](http://124.220.59.85:8080)
- [Yufeng Quant subscription page](https://api.yufeng-quant.com/subscribe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include ranked A-share candidates, individual stock analysis, sector fund-flow summaries, timing scores, token status, and risk reminders.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
