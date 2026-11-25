## Description:

Search Walmart and read product detail, reviews, category listings, buy-box offers, seller storefronts and a seller's catalog as structured JSON, find stores near a US ZIP or Canadian postal code, and target one store's assortment. 8 endpoints; cost depends on the body - 1 credit, or 2 for walmart.com.mx search/category or a store-targeted search/product.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents use this skill to look up Walmart products, prices, reviews, sellers, categories, and store availability for product research and comparison.

### Deployment Geography for Use:

North America (United States, Canada, and Mexico)

## Known Risks and Mitigations:

Risk: Product search details and, for store-targeted lookups, a ZIP or postal code are sent to Scavio.

Mitigation: Before use, consider whether you are comfortable sharing those details with Scavio; omit store targeting when location-specific results are not needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/walmart-product-data)
- [Walmart API documentation](https://scavio.dev/docs/walmart-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=walmart-product-data)
- [Walmart product documentation](https://scavio.dev/docs/walmart-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=walmart-product-data)
- [Walmart stores documentation](https://scavio.dev/docs/walmart-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=walmart-product-data)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON data with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Endpoint-specific results; some endpoints paginate, and credit costs vary by request and marketplace.]

## Skill Version(s):

1.0.6 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
