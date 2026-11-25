## Description:

This skill retrieves thredUP listing prices, estimated retail values, sold listings, product details, and store filters through Scavio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and resale researchers use the skill to look up thredUP prices, item details, and sold listings, and to compare prices with estimated retail across seller types. Sold results show the item's last listed price without a sale date.

### Deployment Geography for Use:

United States and Canada (thredUP's US store; prices in USD)

## Known Risks and Mitigations:

Risk: The skill sends requests to Scavio using an API key.

Mitigation: Use it only if you trust Scavio, and keep SCAVIO_API_KEY in a protected environment variable.

## Reference(s):

- [Scavio thredUP API documentation](https://scavio.dev/thredup-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api)
- [Scavio thredUP search documentation](https://scavio.dev/docs/thredup-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=thredup-api)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [Structured JSON results summarized in concise text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices are in USD; sold listings have no sale date, and one query reaches up to about 2,500 items.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
