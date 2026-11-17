## Description:

Runs a local Python script to fetch current stock prices and related market context for a requested ticker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youpele52](https://clawhub.ai/user/youpele52)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer ticker-specific price questions with current price, daily movement, volume, historical ranges, recent news, and upcoming events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill auto-installs yfinance at runtime, which can introduce supply-chain exposure in higher-trust environments.

Mitigation: Use a pinned dependency or lockfile before deployment where dependency provenance must be controlled.

Risk: The skill queries Yahoo Finance for requested tickers, so results depend on an external market-data provider and network availability.

Mitigation: Treat results as informational market data and confirm critical financial decisions against authoritative sources.

Risk: The skill uses a temporary lock file to serialize execution, which can delay or block concurrent runs if a previous execution stalls.

Mitigation: Run with least-privilege filesystem access and investigate stale locks if execution times out.

## Reference(s):

- [Stock Price Checker Pro on ClawHub](https://clawhub.ai/youpele52/skills/stock-price-checker-pro)
- [Yahoo Finance](https://finance.yahoo.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text stock summary with ticker quote, market statistics, ranges, news links, and upcoming events.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ticker symbol and a runtime with uv; uses yfinance and Yahoo Finance data at execution time.]

## Skill Version(s):

0.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
