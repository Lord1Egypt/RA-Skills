## Description:

Indexes four Wudao A-share market-data subskills that cover 26 real-time API interfaces for quotes, limit-up data, capital-flow analysis, sector rotation, research rankings, and related market intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcdreamjc](https://clawhub.ai/user/jcdreamjc)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill as an index for selecting and configuring Wudao A-share data subskills. It helps route work across market quotes, limit-up analysis, capital-flow analysis, and market-intelligence capabilities that share one API key and base URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires trusting a third-party A-share market-data API service for API-key configuration and downstream data requests.

Mitigation: Confirm the stock.quicktiny.cn service is trusted before installation and configure LB_API_KEY and LB_API_BASE only in the intended environment.

Risk: This package is an index; the actual data-access behavior lives in linked wudao child subskills.

Mitigation: Review and scan each linked wudao-* child skill separately before relying on its outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcdreamjc/skills/wudao-ashare)
- [Wudao market data API service](https://stock.quicktiny.cn)
- [Wudao OpenClaw API base](https://stock.quicktiny.cn/api/openclaw)
- [wudao-market child skill](https://clawhub.ai/skills/wudao-market)
- [wudao-limitup child skill](https://clawhub.ai/skills/wudao-limitup)
- [wudao-analysis child skill](https://clawhub.ai/skills/wudao-analysis)
- [wudao-intel child skill](https://clawhub.ai/skills/wudao-intel)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with links and environment-variable setup details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LB_API_KEY and LB_API_BASE; actual data-access behavior is provided by separately installed child subskills.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
