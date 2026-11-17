## Description:

Trend-following stock analysis using price and volume to produce buy/sell signals, support/resistance levels, and entry/exit targets for Yahoo Finance tickers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddieguan801-oss](https://clawhub.ai/user/eddieguan801-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run command-line technical analysis for a stock ticker, inspect trend status and key levels, and generate entry, target, and stop-loss context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat generated buy/sell signals, targets, and stop-loss values as financial advice.

Mitigation: Present outputs as technical-analysis assistance only and require users to validate against current market data before trading.

Risk: The broad trigger may activate on bare ticker-like symbols when the user did not intend to run stock analysis.

Mitigation: Confirm user intent before running the script or narrow the trigger terms before deployment.

Risk: Runtime behavior depends on the external yfinance package and live Yahoo Finance data availability.

Mitigation: Install in a virtual environment, pin yfinance when deploying, and handle missing or insufficient market data gracefully.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eddieguan801-oss/skills/trend-following)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text console report with trend status, key levels, signals, and entry/target sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ticker and optional period; fetches public Yahoo Finance market data through yfinance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact heading)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
