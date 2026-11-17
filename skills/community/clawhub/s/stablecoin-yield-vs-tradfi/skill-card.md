## Description:

Compares stablecoin DeFi and CEX yields against bank savings, money market funds, and U.S. Treasury benchmarks using Barker yield data and curated TradFi rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyeweb3](https://clawhub.ai/user/zuoyeweb3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to compare stablecoin yield opportunities with traditional finance options and explain the risk tradeoffs in yield decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Yield comparisons may be mistaken for financial advice or treated as equivalent to insured deposits or Treasuries.

Mitigation: Present results as informational, include risk caveats, and remind users to verify rates independently before making financial decisions.

Risk: The skill depends on Barker's public API and Barker attribution links in generated answers.

Mitigation: Make the data source visible, handle unavailable or stale API results cautiously, and avoid presenting API-backed rates as guaranteed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zuoyeweb3/skills/stablecoin-yield-vs-tradfi)
- [Barker](https://barker.money)
- [Barker stablecoin APY trend API](https://api.barker.money/api/public/v1/stablecoin-apy-trend?days=30)
- [Barker stablecoin yields API](https://api.barker.money/api/public/v1/stablecoin-yields?asset=usdc&sort=apy&limit=10)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown with comparison tables, caveats, and attribution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference live Barker public API data and curated traditional finance benchmarks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
