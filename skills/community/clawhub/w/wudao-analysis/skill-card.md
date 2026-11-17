## Description:

悟道 · A股资金分析 helps agents query A-share anomaly detection, capital flow, northbound capital, sector rotation, stock correlation, concept rankings, and concept constituent data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcdreamjc](https://clawhub.ai/user/jcdreamjc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze A-share market activity through the documented stock.quicktiny.cn API endpoints. It is intended for anomaly, money-flow, sector, correlation, and concept analysis rather than K-line charts, limit-up boards, research reports, or news.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock codes, dates, query choices, and authenticated requests are sent to the configured API provider.

Mitigation: Install only if comfortable using stock.quicktiny.cn for A-share analysis, keep LB_API_KEY secret, and avoid reusing sensitive credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcdreamjc/skills/wudao-analysis)
- [stock.quicktiny.cn](https://stock.quicktiny.cn)
- [OpenClaw API base](https://stock.quicktiny.cn/api/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LB_API_KEY and LB_API_BASE environment variables.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
