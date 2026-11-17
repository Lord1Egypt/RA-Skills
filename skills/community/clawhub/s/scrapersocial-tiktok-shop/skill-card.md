## Description:

Retrieves public TikTok Shop product details, reviews, shop catalogues, creator showcases, and search results through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and commerce teams use this skill to examine public TikTok Shop listings, reviews, shop catalogues, and creator promotions or search for products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key is sent as a bearer token to an independent third-party provider.

Mitigation: Use a dedicated ScraperSocial key and share it only if you trust the provider.

Risk: Product and shop URLs, creator handles, searches, and optional flags are sent to ScraperSocial and may consume credits.

Mitigation: Avoid submitting sensitive inputs and check credit costs before making repeated requests.

Risk: Cached responses may not reflect current prices or stock.

Mitigation: Request fresh data when timeliness matters and verify consequential decisions against current listings.

## Reference(s):

- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)
- [ClawHub skill listing](https://clawhub.ai/nikhonit/skills/scrapersocial-tiktok-shop)

## Skill Output:

**Output Type(s):** [JSON data]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include a request ID; paginated results may include a next cursor.]

## Skill Version(s):

1.0.4 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
