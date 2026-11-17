## Description:

悟道 · A股行情数据 helps agents retrieve A-share stock search, K-line, minute-level, ranking, market overview, and trading-calendar data through a configured external market-data API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcdreamjc](https://clawhub.ai/user/jcdreamjc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent query basic China A-share market data, including stock search, K-line history, minute data, rankings, market overview, and trading calendar checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the configured LB_API_KEY to the external stock-data service selected by LB_API_BASE.

Mitigation: Confirm the user trusts stock.quicktiny.cn and the configured LB_API_BASE before installing or using the skill.

Risk: Market interpretation can be mistaken for trading advice.

Mitigation: Treat returned market data and summaries as informational only, not as investment or trading recommendations.

Risk: Limit-up related market fields are available even though the skill excludes limit-up board analysis.

Mitigation: Keep agent responses within the documented basic market-data use case and avoid presenting limit-up board analysis as supported.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcdreamjc/skills/wudao-market)
- [QuickTiny stock service](https://stock.quicktiny.cn)
- [OpenClaw market API base](https://stock.quicktiny.cn/api/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LB_API_KEY and LB_API_BASE environment variables; market data is returned by the configured external API.]

## Skill Version(s):

1.0.1 (source: server release evidence and target metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
