## Description:

Query real-time stablecoin supply APY from Barker's yield index across DeFi protocols and centralized exchanges, returning ranked APY, TVL, protocol, chain, and asset information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyeweb3](https://clawhub.ai/user/zuoyeweb3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up and compare stablecoin yield opportunities by asset, chain, APY, TVL, protocol, and venue. It is intended for informational yield discovery, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stablecoin APY data can fluctuate and may be incomplete or stale when decisions are made.

Mitigation: Treat results as informational, verify rates directly with the venue or protocol, and avoid presenting the output as financial advice.

Risk: Stablecoin yield queries are sent to Barker's public API and responses include Barker attribution.

Mitigation: Use the skill only when this external API dependency and attribution requirement are acceptable for the deployment context.

Risk: Broad yield and stablecoin trigger phrases may activate the skill in general crypto-yield conversations.

Mitigation: Review activation behavior before deployment and invoke it only for stablecoin yield lookup or comparison requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zuoyeweb3/skills/stablecoin-yield-radar)
- [Barker Website](https://barker.money)
- [Barker Public Stablecoin Yields API](https://api.barker.money/api/public/v1/stablecoin-yields)
- [Barker Public API Base](https://api.barker.money/api/public/v1)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown table with concise explanatory text and Barker attribution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include APY, base APY, reward APY, TVL, protocol, chain, asset, pool, and last-updated data returned by Barker's public API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
