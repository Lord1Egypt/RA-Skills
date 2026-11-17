## Description:

Search Wayfair and its US banner sites, retrieve product prices, options, reviews, stock and delivery estimates, and browse current sale events through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and pricing teams can search Wayfair product listings, inspect product and delivery details, and collect repeated readings to build their own price history. Developers can also use the skill to browse categories and current sale events across supported markets.

### Deployment Geography for Use:

United States, Canada, United Kingdom, and Ireland; US banner sites are also supported.

## Known Risks and Mitigations:

Risk: A delivery estimate sends the supplied US ZIP code or Canadian postal code to Scavio; the security guidance notes this may happen without a privacy disclosure.

Mitigation: Provide a ZIP or postal code only when a delivery estimate is needed, and use a location you are comfortable sharing.

Risk: The security scan was partial because some referenced paths could not be resolved, so its evidence is incomplete.

Mitigation: Review the skill and any unresolved referenced files before enabling credentials or relying on its results.

## Reference(s):

- [Scavio Wayfair API overview](https://scavio.dev/wayfair-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=wayfair-api)
- [Wayfair search documentation](https://scavio.dev/docs/wayfair-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=wayfair-api)
- [Wayfair product documentation](https://scavio.dev/docs/wayfair-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=wayfair-api)
- [Wayfair category documentation](https://scavio.dev/docs/wayfair-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=wayfair-api)
- [Wayfair deals documentation](https://scavio.dev/docs/wayfair-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=wayfair-api)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured JSON data with concise explanatory guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices are market-specific; product price applies to the selected option.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
