## Description:

Search public Google Shopping product listings across merchants through ScraperSocial and return pricing data as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhonit](https://clawhub.ai/user/nikhonit)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers, researchers, and developers use this skill to compare publicly listed products and prices across merchants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses a ScraperSocial API key and sends product-search queries to ScraperSocial.

Mitigation: Use a dedicated API key and run the skill only if sharing search queries with ScraperSocial is acceptable.

Risk: Product searches consume credits, and returned prices may be cached.

Mitigation: Set --limit to control credit use; request fresh results and verify prices with merchants when accuracy matters.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nikhonit/skills/scrapersocial-google-shopping)
- [ScraperSocial](https://scrapersocial.com)
- [ScraperSocial OpenAPI specification](https://scrapersocial.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product listings and prices; paginated responses may include a next cursor and request ID.]

## Skill Version(s):

1.0.4 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
