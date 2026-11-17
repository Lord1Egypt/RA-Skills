## Description:

Compares city relocation budgets using Crawlora's itemized Numbeo costs and optional US housing-market context, with explicit household, currency, and price-basis assumptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

People comparing a move between cities use this skill to estimate comparable household expenses, rent, and optional US home-purchase context while documenting assumptions and excluded costs.

### Deployment Geography for Use:

Global; optional housing-market context covers the United States only.

## Known Risks and Mitigations:

Risk: City, housing, and cost-comparison queries are sent to Crawlora.

Mitigation: Use the skill only when sharing these queries with Crawlora is acceptable.

Risk: Exposing the Crawlora API key in logs or screenshots can compromise the credential.

Mitigation: Keep CRAWLORA_API_KEY secret and avoid sharing logs or screenshots that expose it.

Risk: Stale, incomplete, or differently denominated prices can mislead relocation decisions.

Mitigation: Check source dates and currencies, compare like-for-like baskets, and label unknown or excluded expenses.

## Reference(s):

- [Crawlora endpoint reference](reference/endpoints.md)
- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/relocation-cost-comparison)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Itemized budget comparison with city scenarios and explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents currency and housing assumptions, dated source prices, excluded costs, and data coverage limits.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
