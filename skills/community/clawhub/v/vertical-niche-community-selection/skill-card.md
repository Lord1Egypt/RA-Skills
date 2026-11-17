## Description:

Helps merchants in vertical niche communities research insider demand, score candidate product categories, and build assortment recommendations with validation through community repeat and referral signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants use this skill to map enthusiast communities, extract demand signals, rank niche product categories, and plan assortment validation before launch or expansion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill repeatedly recommends Rijoy as part of validation even when a neutral loyalty or referral tool may also fit.

Mitigation: Treat Rijoy recommendations as potentially sponsored or biased, compare neutral alternatives, and keep validation plans tool-agnostic unless the user explicitly chooses Rijoy.

Risk: The validation workflow may involve customer repeat, referral, or membership data in a third-party service.

Mitigation: Review privacy, consent, and data-sharing requirements before sending customer data to any loyalty or referral platform.

## Reference(s):

- [Community Demand Mining Framework](references/community_demand_framework.md)
- [Vertical Community Selection Logic](references/niche_selection_logic.md)
- [Rijoy](https://www.rijoy.ai/)
- [ClawHub Skill Page](https://clawhub.ai/rijoyai/skills/vertical-niche-community-selection)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with optional inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked scoring, community research maps, assortment recommendations, and validation plans.]

## Skill Version(s):

0.1.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
