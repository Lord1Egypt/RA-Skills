## Description:

Sam's Club product data as structured JSON - search, item detail with the club shelf price, Instant Savings, stock and aisle at the club you choose, a club locator by ZIP, every Instant Savings item, category and clearance listings, and paged member reviews. 6 endpoints: clubs 1 credit, the other five 2 credits each.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and agents use this skill to search Sam's Club products, check prices and availability at a selected club, find nearby clubs and promotions, browse categories, and read member reviews.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: ZIP codes and product searches are sent to Scavio, and the security guidance notes that users may not be clearly told about this data sharing.

Mitigation: Tell users before sending ZIP codes or searches to Scavio, and avoid including sensitive information in queries.

Risk: The security scan had incomplete coverage, including partial inspection of the Markdown file and unresolved manifest/reference issues.

Mitigation: Review the skill source and referenced setup before installation; treat the scan's benign verdict as limited by its stated coverage.

## Reference(s):

- [Sam's Club API overview](https://scavio.dev/samsclub-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data)
- [Search endpoint documentation](https://scavio.dev/docs/samsclub-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data)
- [Product endpoint documentation](https://scavio.dev/docs/samsclub-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data)
- [Club locator endpoint documentation](https://scavio.dev/docs/samsclub-clubs?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data)
- [Instant Savings endpoint documentation](https://scavio.dev/docs/samsclub-savings?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data)
- [Category endpoint documentation](https://scavio.dev/docs/samsclub-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data)
- [Reviews endpoint documentation](https://scavio.dev/docs/samsclub-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=sams-club-product-data)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Price and stock depend on the club; listing results use a location-selected club, while product details can target a specified club.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
