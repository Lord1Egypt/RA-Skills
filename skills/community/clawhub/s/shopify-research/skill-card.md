## Description:

Researches public Shopify storefront catalogs, pages, sitemaps, search suggestions, and product recommendations through the Crawlora API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Retail researchers, merchants, and developers use this skill to review public Shopify store products, collections, pages, sitemaps, search suggestions, and recommendations, including supported brand storefronts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested storefront domains, search terms, handles, and the Crawlora API key are sent to Crawlora.

Mitigation: Use only when sharing these inputs with Crawlora is acceptable; keep the API key in CRAWLORA_API_KEY and out of prompts and committed files.

Risk: Successful API requests may consume Crawlora credits.

Mitigation: Scope requests and pagination to the research needed, and check credit usage before larger crawls.

Risk: Brand-specific retail endpoints include J.Crew and Quince catalog, review, and location-style data beyond generic Shopify research.

Mitigation: Review the endpoint reference and request only data relevant to the task; respect storefront terms.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/shopify-research)
- [Crawlora](https://crawlora.net)
- [Endpoint reference](artifact/reference/endpoints.md)

## Skill Output:

**Output Type(s):** [JSON data, Research summaries]

**Output Format:** [JSON responses and natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public storefront data; list results may require pagination.]

## Skill Version(s):

1.0.19 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
