## Description:

Find Walgreens and Duane Reade products, prices, offers, nearby stores, and store stock through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and agents use this skill to find Walgreens products and offers, compare prices, locate nearby stores, and check reported stock by store.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Shopping queries and approximate location are shared with Scavio, and API calls consume credits.

Mitigation: Use a ZIP code when precise coordinates are unnecessary, review credit usage, and enable only the MCP tools you need.

Risk: Exposure of the API key could allow others to use the account's API credits.

Mitigation: Keep SCAVIO_API_KEY in an environment or secret store and out of source code and shared logs.

## Reference(s):

- [Scavio Walgreens API overview](https://scavio.dev/walgreens-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=walgreens-product-data)
- [Walgreens search documentation](https://scavio.dev/docs/walgreens-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=walgreens-product-data)
- [Walgreens product documentation](https://scavio.dev/docs/walgreens-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=walgreens-product-data)
- [Walgreens stores documentation](https://scavio.dev/docs/walgreens-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=walgreens-product-data)
- [Walgreens stock documentation](https://scavio.dev/docs/walgreens-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=walgreens-product-data)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=walgreens-product-data)

## Skill Output:

**Output Type(s):** [JSON data]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product, price, offer, store, and stock fields depend on the requested endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
