## Description:

Vegas T Trading provides Chinese-first A-share and cryptocurrency intraday trading analysis using Vegas Tunnel EMAs, Fibonacci retracement, and multi-period scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georgetao730](https://clawhub.ai/user/georgetao730)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to analyze A-share or cryptocurrency symbols for short-term trading context, including support and resistance levels, multi-period signal alignment, Fibonacci levels, and risk-aware trade planning. Its output should be treated as analytical guidance, not financial advice or an automated trading signal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill prints trading recommendations and confidence-style signals that could be mistaken for financial advice.

Mitigation: Treat outputs as informational analysis only, require independent review, and do not use them as automated trade-execution signals.

Risk: The analyzer depends on third-party Python market-data packages and live network data.

Mitigation: Install in an isolated Python environment, pin akshare and pandas versions where possible, and validate data freshness before relying on results.

Risk: Cryptocurrency data coverage is effectively Binance-only.

Mitigation: Disclose the exchange limitation and compare against another data source when coverage or pricing differences matter.

Risk: The skill is Chinese-first and may be less usable for readers expecting English-only output.

Mitigation: Confirm that operators can review Chinese-language reports or translate the output before making decisions from it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/georgetao730/skills/vegas-t-trading)
- [Publisher profile](https://clawhub.ai/user/georgetao730)

## Skill Output:

**Output Type(s):** [analysis, markdown, json, shell commands, guidance]

**Output Format:** [Chinese text trading report or JSON, often with shell commands for running the analyzer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a market symbol and optional period, market, exchange, multi-period, volume-check, and output-format parameters.]

## Skill Version(s):

1.3.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
