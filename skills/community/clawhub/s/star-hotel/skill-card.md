## Description:

Smart hotel search, supporting filtering by location, date, star rating, and budget

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxc-aqr](https://clawhub.ai/user/zxc-aqr)

### License/Terms of Use:


## Use Case:

External users and travel-planning agents use this skill to search hotels, retrieve room prices, and fetch search tags from Star Hotel MCP using structured location, date, rating, budget, and amenity filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel search details are sent to a third-party MCP service.

Mitigation: Send only structured hotel search fields needed for the request, such as location, dates, occupancy, rating, budget, and tags.

Risk: Queries may contain personal information that is not needed for hotel search.

Mitigation: Remove names, phone numbers, emails, IDs, local file details, system information, and unrelated private text before calling the MCP tools.

Risk: Hotel price, room, currency, language, date, and identity details can affect booking decisions.

Mitigation: Confirm currency, language, country, dates, hotel identity, and room details when results matter.

Risk: The bundled public API key may be rate-limited or less accountable than a personal key.

Mitigation: Use an exclusive Star Hotel key for higher quotas or clearer operational accountability.

## Reference(s):

- [Star Hotel Search on ClawHub](https://clawhub.ai/zxc-aqr/skills/star-hotel)
- [zxc-aqr Publisher Profile](https://clawhub.ai/user/zxc-aqr)
- [Star Hotel MCP Application](https://mcp.agentichotel.cn/apply)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown guidance with JSON tool-call examples and structured hotel result schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces hotel search parameters, hotel detail requests, tag retrieval calls, and guidance for filtering personal information before sending requests.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
