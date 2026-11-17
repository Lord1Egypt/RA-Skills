## Description:

Simple technical analysis for stocks that fetches Yahoo Finance data and calculates SMA20, SMA50, 14-day RSI, 20-day price-range position, and buy, hold, or sell-style signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loda13](https://clawhub.ai/user/loda13)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to run a lightweight stock technical analysis script for supported or Yahoo Finance-compatible tickers. The output helps review technical indicators, but it is educational analysis and not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script contacts Yahoo Finance at runtime to fetch stock chart data.

Mitigation: Run it only in environments where outbound access to Yahoo Finance is acceptable.

Risk: The output includes buy, hold, or sell-style technical signals that could be mistaken for investment advice.

Mitigation: Treat the results as educational technical analysis and apply independent financial review before making decisions.

Risk: The documentation describes custom ticker arguments, but the inspected script uses a fixed stock list.

Mitigation: Review or update the script before relying on custom ticker command-line input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loda13/skills/stock-tech-analysis)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text output with stock prices, technical indicators, and summary signals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public Yahoo Finance chart data at runtime and prints analysis in Chinese.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
