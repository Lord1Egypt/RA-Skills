## Description:

Helps agents research Zara categories, products, search suggestions, and nearby stores through the Crawlora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and shopping assistants use this skill to browse Zara's US catalog, compare product details and availability, and find nearby stores without scraping Zara pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Catalog searches and store-lookup coordinates are sent to Crawlora, a third-party API provider.

Mitigation: Use only if comfortable with Crawlora processing these requests; avoid sensitive personal data in queries and share coordinates only when needed.

Risk: Exposing the Crawlora API key could allow unauthorized use.

Mitigation: Keep the key in CRAWLORA_API_KEY and never include it in queries, source files, or commits.

## Reference(s):

- [Zara endpoint reference](reference/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/zara-research)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown responses informed by structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers the US storefront; search results can include broader recommendations rather than exact keyword matches.]

## Skill Version(s):

1.0.16 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
