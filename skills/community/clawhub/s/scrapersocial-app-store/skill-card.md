## Description:

Retrieves public Apple App Store app details, reviews, keyword search results, category listings, and storefront locations through ScraperSocial.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and app marketers use this skill to research public App Store listings, review feedback, search visibility, and category rankings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends the ScraperSocial API key to a third-party service.

Mitigation: Use only an authorized ScraperSocial key and enable the skill only if sharing it with api.scrapersocial.com is acceptable.

Risk: Requests may consume ScraperSocial credits, particularly for paginated results.

Mitigation: Set a reasonable result limit and page only as needed before making repeated requests.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nikhonit/skills/scrapersocial-app-store)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public App Store data; paginated responses can include a cursor and responses include a request ID.]

## Skill Version(s):

1.0.4 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
