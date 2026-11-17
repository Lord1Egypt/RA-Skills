## Description:

Search Spec's Wines, Spirits & Finer Foods in Texas for products, prices, stock across stores, and regional store locations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find Spec's products, compare online and store-level prices and stock, and locate stores in Texas.

### Deployment Geography for Use:

Texas, United States

## Known Risks and Mitigations:

Risk: Search terms and store selections are sent to Scavio, and API calls consume credits.

Mitigation: Tell users that lookups are sent to Scavio and may use credits before making requests.

Risk: The API key could be exposed if placed in shared files or source code.

Mitigation: Keep SCAVIO_API_KEY in an environment variable or secret store, not in shared files.

## Reference(s):

- [Spec's product API documentation](https://scavio.dev/docs/specs-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=specs-liquor-prices)
- [Spec's search API documentation](https://scavio.dev/docs/specs-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=specs-liquor-prices)
- [Spec's store locator API documentation](https://scavio.dev/docs/specs-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=specs-liquor-prices)
- [Spec's API overview](https://scavio.dev/specs-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=specs-liquor-prices)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON with product search results, product details, store prices, inventory, and store locations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live API results; prices are expressed in cents and each endpoint consumes 5 credits.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
