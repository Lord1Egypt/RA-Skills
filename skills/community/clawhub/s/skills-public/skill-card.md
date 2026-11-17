## Description:

Helps agents look up current stock quotes for A-shares, Hong Kong stocks, and U.S. stocks from a user-provided stock name or ticker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianweig200-commits](https://clawhub.ai/user/jianweig200-commits)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to identify a requested stock and return current quote details such as price, price change, trading range, volume, turnover, and market capitalization when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock prices returned by web search or public finance endpoints may be delayed, unavailable, or inaccurate.

Mitigation: Treat the output as informational and verify prices with a trusted market-data source before making trading decisions.

Risk: Market-specific handling and public data endpoints can fail or return incomplete quote fields.

Mitigation: Retry failed lookups and check critical fields against the relevant exchange or market-data provider.

## Reference(s):

- [Stock API Reference](references/stock-api.md)
- [ClawHub skill page](https://clawhub.ai/jianweig200-commits/skills/skills-public)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text quote summary, with optional JSON search-query output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stock name, ticker, current price, price change, highs and lows, open and previous close, volume, turnover, and market capitalization when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
