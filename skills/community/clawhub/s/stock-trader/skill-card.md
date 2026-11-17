## Description:

A股股票交易助手 helps agents query A-share prices and market news, analyze potential stocks, sector fund flows, leaders, and sentiment, and run an aggressive simulated trading workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunxianzheng](https://clawhub.ai/user/sunxianzheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect A-share market data, summarize stock and sector signals, generate trading-oriented analysis, set price alerts, and maintain simulated trading reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The price alert feature creates recurring OpenClaw jobs that message a hard-coded QQ recipient.

Mitigation: Remove or replace the hard-coded recipient with the user's confirmed destination before enabling alerts.

Risk: The simulation reset workflow writes to a fixed trading-state path and can overwrite existing state.

Mitigation: Verify the state path and back up trading records before running the reset command.

Risk: Stock analysis and simulated trading outputs may be mistaken for investment advice.

Mitigation: Present outputs as informational analysis only and require human review before any financial decision.

## Reference(s):

- [Technical indicators reference](references/indicators.md)
- [ClawHub skill page](https://clawhub.ai/sunxianzheng/skills/stock-trader)
- [Tencent quote endpoint used by scripts](https://qt.gtimg.cn/q={stock_code})
- [Sina Finance stock news source](https://finance.sina.com.cn/stock/)
- [Eastmoney industry fund-flow source](https://资金流向.eastmoney.com/IndustryRank/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands and tabular analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local JSON trading-state records and OpenClaw cron alert configuration.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
