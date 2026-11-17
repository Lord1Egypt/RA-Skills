## Description:

Get a real-time stablecoin market overview from 500+ protocols and 20+ CEX, including market cap, yield-bearing market cap, asset and chain distribution, and market-wide APY statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyeweb3](https://clawhub.ai/user/zuoyeweb3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to answer stablecoin market overview questions with Barker public API data, including market capitalization, TVL distribution, chain distribution, and APY trend comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Responses depend on Barker as the market-data source and may reflect that source's coverage, availability, and attribution requirements.

Mitigation: Use the skill when Barker-sourced stablecoin market data is acceptable, and preserve the Barker attribution described by the skill.

Risk: Generic market questions could trigger the skill even when the user is not asking about stablecoins.

Mitigation: Apply the skill only when the request is about stablecoins, stablecoin market capitalization, stablecoin TVL, or stablecoin yield trends.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zuoyeweb3/skills/stablecoin-market-brief)
- [Barker website](https://barker.money)
- [Stablecoin market API](https://api.barker.money/api/public/v1/stablecoin-market)
- [Stablecoin APY trend API](https://api.barker.money/api/public/v1/stablecoin-apy-trend?days=90)
- [Barker public API base](https://api.barker.money/api/public/v1)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary with ranked lists, numeric market metrics, and Barker attribution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Barker public API endpoints for current market and APY trend data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
