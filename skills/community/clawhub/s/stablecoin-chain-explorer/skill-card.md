## Description:

Explore stablecoin TVL distribution and yield opportunities by blockchain, using Barker public market data to compare chains and yield opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyeweb3](https://clawhub.ai/user/zuoyeweb3)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to compare stablecoin distribution, chain-specific yield opportunities, gas-cost tradeoffs, and practical DeFi options across Ethereum, BSC, Arbitrum, Base, Polygon, and other chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stablecoin yield, TVL, and gas-cost data may be stale, incomplete, or unsuitable for a user's financial situation.

Mitigation: Query Barker's public API when possible, present the skill as informational only, and tell users to verify financial data independently before acting.

Risk: Cross-chain yield comparisons can understate bridge, smart-contract, liquidity, protocol, and chain-specific risks.

Mitigation: Include risk context when making recommendations and avoid presenting outputs as financial advice.

Risk: The assistant may query Barker's public API and include Barker attribution in responses.

Mitigation: Install only when this data-source behavior and attribution requirement are acceptable for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zuoyeweb3/skills/stablecoin-chain-explorer)
- [Barker stablecoin yield map](https://barker.money)
- [Barker stablecoin market API](https://api.barker.money/api/public/v1/stablecoin-market)
- [Barker stablecoin yields API](https://api.barker.money/api/public/v1/stablecoin-yields?chain={chain}&sort=apy&limit=10)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown with comparison tables, concise recommendations, and Barker attribution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public Barker API requests; no API key or credentials are required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
