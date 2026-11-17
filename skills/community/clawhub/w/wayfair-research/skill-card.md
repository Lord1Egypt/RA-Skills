## Description:

Browses Wayfair categories and retrieves category product grids and product details through Crawlora as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers, researchers, and developers can browse Wayfair categories, compare listed products, and retrieve product prices, availability, ratings, and variants by product ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Category and product lookups are sent to an external Crawlora service.

Mitigation: Use only for public Wayfair category and product data when external processing is acceptable.

Risk: The service requires a user-provided API key.

Mitigation: Set CRAWLORA_API_KEY in the environment; do not log, share, or commit it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crawlora-org/skills/wayfair-research)
- [Wayfair endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON product data or a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Category listings are paginated; category names are derived from URL slugs. No full-text product search or reviews endpoint.]

## Skill Version(s):

1.0.17 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
