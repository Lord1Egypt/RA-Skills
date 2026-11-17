## Description:

Helps agents retrieve Realtor.com listings, sold comparables, property details, market statistics, locations, and agent profiles through Scavio's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Real estate professionals and developers use this skill to research U.S. listings and sold comparables, inspect properties and valuations, compare local markets, and find agents.

### Deployment Geography for Use:

Global (U.S. property data)

## Known Risks and Mitigations:

Risk: Property searches, addresses, listing URLs, and agent lookups are sent to Scavio/Realtor.com under the user's API key.

Mitigation: Share only necessary query details and avoid including personal information that is not needed for the lookup.

Risk: API searches and pagination may consume paid credits.

Mitigation: Check credit costs and agree on a budget before running loops or broad searches.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/realtor-com-property-data)
- [Scavio Realtor.com search documentation](https://scavio.dev/docs/realtor-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=realtor-com-property-data)
- [Scavio Realtor.com API overview](https://scavio.dev/realtor-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=realtor-com-property-data)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=realtor-com-property-data)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Code]

**Output Format:** [Markdown guidance with structured JSON results and optional API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include listing links, prices, property histories, market statistics, and agent profiles.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
