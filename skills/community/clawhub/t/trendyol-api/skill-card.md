## Description:

Connects to Trendyol storefronts to retrieve product and seller prices, listings, reviews, rankings, promotions, and delivery estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to retrieve and compare Trendyol product listings and seller offers, and to inspect marketplace reviews, rankings, promotions, and delivery estimates. It supports 35 storefront markets and returns each market's data in its local currency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and any supplied delivery-location identifiers are sent to Scavio.

Mitigation: Avoid including sensitive search terms or unnecessary delivery-location details in requests.

Risk: The security scan had partial coverage because some referenced local paths were missing.

Mitigation: Review the complete release sources before deployment where those missing paths are available.

## Reference(s):

- [Trendyol API skill release](https://clawhub.ai/scavio-ai/skills/trendyol-api)
- [Scavio Trendyol search API documentation](https://scavio.dev/docs/trendyol-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=trendyol-api)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON marketplace data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live listings, prices, seller details, reviews, rankings, promotions, and delivery estimates; prices are reported in each storefront's local currency.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
