## Description:

Retrieves public Amazon product details, search results, reviews, and seller listings through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can look up public Amazon listings, compare sellers, search for products, and summarize customer reviews for product research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product URLs, search terms, and the API key are sent to ScraperSocial.

Mitigation: Use only if sharing these inputs with ScraperSocial is acceptable; keep the API key private.

Risk: Search, reviews, and seller requests may consume credits per result.

Mitigation: Set result limits and request only the data needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nikhonit/skills/scrapersocial-amazon)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON data or natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paginated responses may include a cursor; API responses include a request ID.]

## Skill Version(s):

1.0.4 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
