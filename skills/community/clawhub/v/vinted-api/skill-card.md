## Description:

Provides structured JSON access to Vinted listings across 27 markets, including search, listing details, public seller information, brands, filters, categories, and autocomplete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and shopping research agents use it to find live Vinted listings, compare asking prices by market, inspect listing details and public seller information, and build new listing alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill requires sending its Vinted-related request data to api.scavio.dev and providing a Scavio API key; the security scan was benign with medium confidence but partial.

Mitigation: Before installing, confirm that you trust api.scavio.dev and are comfortable providing its API key and sending the described request data there; account for the incomplete scan evidence.

## Reference(s):

- [Vinted API overview](https://scavio.dev/vinted-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api)
- [Vinted search documentation](https://scavio.dev/docs/vinted-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api)
- [Vinted product documentation](https://scavio.dev/docs/vinted-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api)
- [Vinted seller documentation](https://scavio.dev/docs/vinted-seller?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api)
- [Vinted seller products documentation](https://scavio.dev/docs/vinted-seller-products?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api)
- [Vinted seller feedback documentation](https://scavio.dev/docs/vinted-seller-feedback?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api)
- [Vinted brands documentation](https://scavio.dev/docs/vinted-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api)
- [Vinted suggestions documentation](https://scavio.dev/docs/vinted-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api)
- [Vinted filters documentation](https://scavio.dev/docs/vinted-filters?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api)
- [Vinted categories documentation](https://scavio.dev/docs/vinted-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON data with accompanying usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Marketplace listings, asking prices and buyer fees, product and public seller details, brand and filter data, categories, and autocomplete results.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
