## Description:

Search Target.com, browse a category, read product detail by TCIN, pull reviews with the rating breakdown, and check in-store stock at every Target near a ZIP as structured JSON. 5 endpoints, 1 credit each, store-aware pricing via store_id.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Target product search and category results, product details, reviews, and store availability through Scavio. It returns structured data for product research and comparisons.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Searches, product identifiers, and any supplied ZIP or store selection are sent to Scavio; its live behavior and data-retention practices were not independently verified.

Mitigation: Share only information you are comfortable sending to the provider and review its current privacy practices before use.

Risk: API requests use account credits and require an API key.

Mitigation: Protect SCAVIO_API_KEY and monitor credit usage.

## Reference(s):

- [Target search API documentation](https://scavio.dev/docs/target-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=target-product-data)
- [Target category API documentation](https://scavio.dev/docs/target-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=target-product-data)
- [Target product API documentation](https://scavio.dev/docs/target-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=target-product-data)
- [Target reviews API documentation](https://scavio.dev/docs/target-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=target-product-data)
- [Target availability API documentation](https://scavio.dev/docs/target-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=target-product-data)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=target-product-data)

## Skill Output:

**Output Type(s):** [JSON, Product data]

**Output Format:** [Structured JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product search and category results, product details, review summaries, or store availability; data is returned from the selected endpoint.]

## Skill Version(s):

1.0.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
