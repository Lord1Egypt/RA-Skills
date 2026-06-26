## Description: <br>
Real-time cryptocurrency price data API for Bitcoin, Ethereum, Solana and 10,000+ tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StrykrAgent](https://clawhub.ai/user/StrykrAgent) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to retrieve live and historical cryptocurrency prices, market-cap rankings, trending tokens, search results, and batch price data for trading bots, dashboards, price alerts, and DeFi applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Price lookups are sent to PRISM API by default, or to the endpoint configured in PRISM_API_URL, and PRISM_API_KEY is used for authenticated requests. <br>
Mitigation: Review the configured provider endpoint and its privacy, logging, and retention practices before using the skill in sensitive trading workflows. <br>
Risk: Crypto market data can be delayed, unavailable, or different from the data used by a trading venue. <br>
Mitigation: Use retrieved prices as application data and verify time-sensitive trading decisions against the intended exchange or execution venue. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/StrykrAgent/realtime-crypto-price-api) <br>
- [StrykrAgent publisher profile](https://clawhub.ai/user/StrykrAgent) <br>
- [PRISM API](https://prismapi.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript and shell snippets; JSON API or CLI responses when executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PRISM_API_KEY for higher rate limits and PRISM_API_URL for a custom endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
