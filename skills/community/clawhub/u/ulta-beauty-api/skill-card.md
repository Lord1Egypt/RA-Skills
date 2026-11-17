## Description:

Search Ulta Beauty products and categories, retrieve pricing and product details, and check shade availability for pickup at nearby stores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can use this skill to find Ulta Beauty products, compare prices and variants, inspect product details and recent reviews, and check pickup stock near a US ZIP code.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Searches and nearby inventory lookups send the query or selected product and ZIP code to Scavio.

Mitigation: Use only the product details and ZIP needed for the lookup, and avoid including sensitive information in searches.

Risk: Each endpoint request uses one API credit, and requests require the SCAVIO_API_KEY credential.

Mitigation: Protect the API key and account for credit use when making repeated searches or lookups.

## Reference(s):

- [Scavio Ulta Beauty API Overview](https://scavio.dev/ulta-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=ulta-beauty-api)
- [Ulta Search API Documentation](https://scavio.dev/docs/ulta-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=ulta-beauty-api)
- [Ulta Category API Documentation](https://scavio.dev/docs/ulta-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=ulta-beauty-api)
- [Ulta Product API Documentation](https://scavio.dev/docs/ulta-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=ulta-beauty-api)
- [Ulta Store Stock API Documentation](https://scavio.dev/docs/ulta-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=ulta-beauty-api)
- [ClawHub Skill Page](https://clawhub.ai/scavio-ai/skills/ulta-beauty-api)

## Skill Output:

**Output Type(s):** [JSON data, Product and pricing information, Store availability information]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product listings, product details, variants, prices, ratings, recent reviews, fulfillment options, and nearby store stock; live retail values may change.]

## Skill Version(s):

1.0.0 (source: frontmatter; server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
