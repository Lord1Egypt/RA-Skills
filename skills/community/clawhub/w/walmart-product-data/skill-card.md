## Description:

Search Walmart products and retrieve product details, reviews, categories, buy-box offers, seller listings, and nearby stores through Scavio's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and shopping or retail research agents use this skill to look up Walmart products, compare prices and reviews, inspect sellers and buy-box offers, and check store-specific assortment in the US and Canada.

### Deployment Geography for Use:

United States, Canada, and Mexico (supported Walmart marketplaces; store targeting is limited to the US and Canada)

## Known Risks and Mitigations:

Risk: Search terms, product and seller IDs, and ZIP or postal codes are sent to a third-party API.

Mitigation: Use only with approval to share these inputs with Scavio; avoid sensitive or unnecessary location details.

Risk: An exposed API key could permit unauthorized use.

Mitigation: Keep SCAVIO_API_KEY in an environment variable or secret store; do not commit it to source control.

Risk: Results can be incomplete or mistaken for a full offer list, and requests consume credits.

Mitigation: Check warnings and credits used, confirm product links and store location, and describe buy-box results as one seller only.

## Reference(s):

- [Scavio Walmart API documentation](https://scavio.dev/docs/walmart-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=walmart-product-data)
- [Walmart stores documentation](https://scavio.dev/docs/walmart-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=walmart-product-data)
- [Walmart reviews documentation](https://scavio.dev/docs/walmart-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=walmart-product-data)
- [Walmart offers documentation](https://scavio.dev/docs/walmart-offers?utm_source=agent-skills&utm_medium=skill&utm_campaign=walmart-product-data)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Product summaries and links in text or Markdown, based on structured JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include prices, availability, ratings, reviews, seller data, and store location; API calls consume credits.]

## Skill Version(s):

1.0.4 (source: server-resolved ClawHub release; skill frontmatter states 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
