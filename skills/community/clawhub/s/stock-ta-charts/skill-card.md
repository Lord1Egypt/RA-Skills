## Description:

Generate professional technical analysis charts with candlesticks, Fibonacci levels, SMA 20/50, RSI, and pattern detection for selected crypto and commodities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nomadrex](https://clawhub.ai/user/nomadrex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-analysis agents use this skill to generate technical-analysis chart images and short indicator summaries for BTC, ETH, XRP, SUI, gold, and silver.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill executes a local Python module that is not included in the release artifact.

Mitigation: Review and trust the local ~/clawd/crypto_charts.py file before installing or running the skill.

Risk: The artifact includes an example command that sends generated charts to a fixed Telegram recipient.

Mitigation: Replace the hard-coded recipient with a user-chosen, confirmed destination before sending any chart.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nomadrex/skills/stock-ta-charts)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Text, Guidance]

**Output Format:** [Markdown with inline shell commands and generated PNG chart file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates chart images from local market-data tooling and may print price, RSI, and detected pattern summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
