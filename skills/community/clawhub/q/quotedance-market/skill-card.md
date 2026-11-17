## Description:

Generates structured Chinese-language global market intelligence reports by combining market quotes, sector leaders, and professional news sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoocky](https://clawhub.ai/user/yoocky)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate daily or weekend global market intelligence reports covering equities, futures, themes, opportunities, and risks. The report is for market research and operational briefing, not personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated proxy URLs or quotedance API keys may be exposed through network diagnostics, logs, or process arguments.

Mitigation: Avoid --net-debug with credential-bearing proxy URLs, use narrowly scoped or disposable API keys, and review logs before sharing output.

Risk: Curl fallback can pass proxy details through command arguments.

Mitigation: Disable curl fallback or use non-sensitive proxy credentials until the fallback path avoids exposing secrets.

Risk: Market data and news sources may be unavailable, delayed, blocked, or rate-limited.

Mitigation: Treat generated reports as research briefings, check source availability, and verify important market data before acting on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yoocky/skills/quotedance-market)
- [Publisher profile](https://clawhub.ai/user/yoocky)
- [quotedance service endpoint](https://quotedance.api.gapgap.cc)
- [Yahoo Finance quote API](https://query1.finance.yahoo.com/v7/finance/quote)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown market report with console logs and JSON cache snapshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs a weekday or weekend report based on the current date and stores market/news snapshots under the skill memory directory.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
