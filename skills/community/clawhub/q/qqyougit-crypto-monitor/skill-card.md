## Description:

This skill helps agents query cryptocurrency prices, store local price alert settings, and generate concise market reports from public market-data APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check BTC, ETH, SOL, and other cryptocurrency prices, create local price-threshold alert records, and produce informational market summaries. It is not for trade execution, DeFi operations, wallet management, or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect dependable continuous alert delivery, but the release evidence says the skill saves alert settings without shipping a working continuous monitor or notification sender.

Mitigation: Use alert records as configuration only unless a separate monitored scheduler and notification path are reviewed and deployed.

Risk: Market reports can sound action-oriented even though the skill is not intended to provide investment advice.

Mitigation: Treat generated reports as informational market summaries and require independent financial review before acting on them.

Risk: Price checks and reports depend on third-party market-data APIs and may fail, lag, or return incomplete data.

Mitigation: Check timestamps and data source labels, and confirm material decisions against another trusted source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/qqyougit-crypto-monitor)
- [加密货币监控与告警 - 详细内容](references/details.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown or terminal text with price data, alert confirmations, report summaries, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include locally saved alert settings under the user's OpenClaw workspace; market data is informational and depends on third-party API availability.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
