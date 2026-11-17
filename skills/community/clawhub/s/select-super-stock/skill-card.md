## Description:

A Chinese-language A-share single-stock research assistant that verifies completed daily bars, trend indicators, and data gaps for a specified six-digit A-share symbol without screening stocks or giving buy/sell advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georgetao730](https://clawhub.ai/user/georgetao730)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run a local Python helper for source-dated, non-real-time A-share daily-bar research on one explicitly supplied stock code. It is intended for learning and informational review of verifiable technical observations, not investment advice, ranking, portfolio management, or trading automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public daily market data may be delayed, rate-limited, unavailable, or revised.

Mitigation: The skill records source, trade date, collection time, and adjustment basis, and stops stock conclusions when calendar, OHLCV, history length, or source checks fail.

Risk: Technical observations may be mistaken for investment advice or a trading recommendation.

Mitigation: Outputs separate observations from conclusions, omit scores, rankings, target prices, position sizing, and buy/sell language, and include an informational-use disclaimer.

Risk: Running the helper performs local script execution and network collection through AKShare.

Mitigation: Review the script before installation or execution; server security evidence states it does not install dependencies, read credentials, place trades, manage accounts, or perform hidden persistent behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/georgetao730/skills/select-super-stock)
- [Data and research boundary](artifact/references/data-policy.md)
- [Risk boundary](artifact/references/risk-boundary.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text report or structured JSON, with usage shown as Markdown shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output includes source, symbol, trade date, collection time, adjustment basis, non-real-time daily-data notice, missing coverage, and an informational-use disclaimer.]

## Skill Version(s):

1.4.0 (source: server release metadata and script VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
