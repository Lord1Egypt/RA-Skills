## Description:

Retrieves Tractor Supply product prices, inventory, fulfillment options, store details, and product listings through Scavio's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check current Tractor Supply prices by store or ZIP, compare prices across stores, check reported stock and fulfillment options, and find products or store information.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: ZIP codes and shopping queries used for lookups may be shared with Scavio, a third party.

Mitigation: Use ZIP-based lookups only if you are comfortable sharing the ZIP and shopping query with Scavio.

## Reference(s):

- [Scavio Tractor Supply API overview](https://scavio.dev/tractorsupply-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api)
- [Store prices API documentation](https://scavio.dev/docs/tractorsupply-store-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api)
- [Store stock API documentation](https://scavio.dev/docs/tractorsupply-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api)
- [Fulfillment API documentation](https://scavio.dev/docs/tractorsupply-fulfillment?utm_source=agent-skills&utm_medium=skill&utm_campaign=tractor-supply-prices-api)
- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/tractor-supply-prices-api)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices and availability are current to the API response; price and stock history are not provided.]

## Skill Version(s):

1.0.0 (source: server-resolved release, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
