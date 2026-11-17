## Description:

Binance cryptocurrency trading research, technical analysis, DCA planning, position sizing, market scanning, and whale activity support for crypto market questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fpsjago](https://clawhub.ai/user/fpsjago)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to research Binance crypto markets, retrieve public market data, calculate indicators, plan DCA schedules, size positions, scan USDT pairs, and assess whale or orderbook activity. Treat outputs as research support, not financial advice or automated trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading analysis, MACD-based signals, and position sizing calculations may be wrong or unsuitable for a user's financial situation.

Mitigation: Treat outputs as educational research, independently verify calculations and signals, and avoid risking money based only on the skill output.

Risk: Authenticated Binance API examples could be misused with keys that allow live trading.

Mitigation: Do not provide Binance API keys with trading permissions; use read-only credentials or public endpoints for research workflows.

Risk: The artifact includes a VPN bypass suggestion for Binance API access errors.

Mitigation: Do not bypass local access restrictions; use only compliant data access methods for the user's jurisdiction.

## Reference(s):

- [Trading Research ClawHub listing](https://clawhub.ai/fpsjago/skills/trading-research)
- [Binance API Quick Reference](references/binance-api.md)
- [Technical Indicators Reference](references/indicators.md)
- [Trading Strategies Reference](references/strategies.md)
- [Binance Spot REST API](https://api.binance.com)
- [Binance Futures REST API](https://fapi.binance.com)
- [Binance Data API](https://data-api.binance.vision)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, numeric analysis, and optional JSON from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Binance public REST endpoints for market data; authenticated trading setup is referenced, but the skill states it does not execute trades.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
