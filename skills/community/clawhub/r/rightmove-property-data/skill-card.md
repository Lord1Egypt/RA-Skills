## Description:

Helps agents retrieve structured UK property listings, listing details, England and Wales sold-price histories, locations, and estate agent branches through Scavio's Rightmove API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Property researchers, estate agents, and developers use this skill to search UK homes for sale or rent, inspect listings and agent branches, and compare historical sale prices for addresses in England and Wales.

### Deployment Geography for Use:

Global use for UK property research; sold-price coverage is limited to England and Wales.

## Known Risks and Mitigations:

Risk: Property searches, postcodes, addresses, listing URLs, and filters are sent to Scavio's API.

Mitigation: Obtain user consent before external lookups involving private property details and share only necessary inputs.

Risk: API requests spend credits, and exposing the API key could enable unauthorized usage.

Mitigation: Keep SCAVIO_API_KEY in an environment variable or secret store, never hardcode real keys, and check credit usage before bulk queries.

Risk: Sold-price records lag by about two months and results have page caps, so recent or exhaustive claims may be misleading.

Mitigation: Check data coverage dates and pagination totals, and qualify any incomplete or recent-sale results.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/rightmove-property-data)
- [Scavio Rightmove search documentation](https://scavio.dev/docs/rightmove-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=rightmove-property-data)
- [Scavio Rightmove sold-price documentation](https://scavio.dev/docs/rightmove-sold?utm_source=agent-skills&utm_medium=skill&utm_campaign=rightmove-property-data)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=rightmove-property-data)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance and structured JSON property data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Property listings, sale histories, and agent details include source URLs for verification.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
