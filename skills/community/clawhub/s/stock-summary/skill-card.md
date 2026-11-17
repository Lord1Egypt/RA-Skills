## Description:

Query stock quotes, technical indicators, trading posture, and a trend chart for A-share, Hong Kong, and US stock codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongdong-bryant](https://clawhub.ai/user/dongdong-bryant)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve stock quote summaries, RSI/MACD technical analysis, buy/sell/hold posture, and a one-month trend chart for supported stock codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce unreliable trading signals from rough technical indicators and live data routing issues.

Mitigation: Treat buy/sell/hold posture as non-personalized technical commentary and verify quotes, indicators, and investment decisions with authoritative financial sources.

Risk: Chart generation writes to a fixed privileged path.

Mitigation: Review or adjust the chart output path before deployment so generated files are written only to an approved workspace location.

Risk: A-share quote requests use unencrypted HTTP endpoints.

Mitigation: Validate returned market data and prefer trusted or encrypted data sources where available before relying on the summary.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dongdong-bryant/skills/stock-summary)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown-style text summary with quote fields, RSI/MACD values, a buy/sell/hold posture, and a generated PNG trend chart path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires one stock code input; output depends on live market data from East Money or Yahoo Finance/yfinance sources.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
