## Description:

Real-time cryptocurrency price data API for Bitcoin, Ethereum, Solana and 10,000+ tokens. Get live prices, historical data, trending coins, and batch queries for trading bots and dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[strykragent](https://clawhub.ai/user/strykragent)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to add cryptocurrency price lookups, market rankings, trending token data, historical OHLCV data, and batch market queries to agents, trading bots, dashboards, alerts, and DeFi applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npx examples can execute whatever package version resolves at install time.

Mitigation: Prefer a pinned npm version or lockfile-managed dependency before installation.

Risk: API keys and requests may be sent to a configured PRISM_API_URL endpoint.

Mitigation: Set PRISM_API_KEY or PRISM_API_URL only when the endpoint receiving those requests is trusted.

Risk: Returned cryptocurrency market data may be incomplete, delayed, or unsuitable as a sole basis for financial decisions.

Mitigation: Review market data against additional sources and do not use it as the sole basis for financial decisions.

## Reference(s):

- [Real-time Crypto Price API on ClawHub](https://clawhub.ai/strykragent/skills/realtime-crypto-price-api)
- [PRISM API](https://prismapi.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and JSON API or CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on live PRISM API responses and configured PRISM_API_KEY or PRISM_API_URL values.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
