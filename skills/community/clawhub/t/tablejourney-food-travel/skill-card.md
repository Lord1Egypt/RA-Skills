## Description:

Answer food travel questions with TableJourney's verified data (places, festivals with dates, dishes, itineraries, bookable experiences, stays and car hire) through its public REST API or MCP server, citing the page and passing booking links unchanged.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lewismvaughan](https://clawhub.ai/user/lewismvaughan)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and trip planners use this skill to find places to eat, food festivals, local dishes, itineraries, and bookable travel experiences in covered cities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel searches may involve destination, dates, and personal preferences.

Mitigation: Share only the destination, dates, and preferences needed for the search.

Risk: Booking links use affiliate redirects and may earn TableJourney a commission.

Mitigation: Disclose the affiliate relationship and pass booking links through unchanged; the user completes purchases themselves.

## Reference(s):

- [TableJourney MCP server](https://tablejourney.com/mcp)
- [MCP manifest](https://tablejourney.com/.well-known/mcp.json)
- [TableJourney REST API](https://tablejourney.com/api/v1)
- [REST API OpenAPI specification](https://tablejourney.com/api/v1/openapi.json)
- [REST API documentation](https://tablejourney.com/api/v1/docs)
- [Authentication and API key information](https://tablejourney.com/auth.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown answers with cited source pages and unchanged booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise recommendations grounded in service results; discloses affiliate booking links and avoids bulk-copied listings.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
