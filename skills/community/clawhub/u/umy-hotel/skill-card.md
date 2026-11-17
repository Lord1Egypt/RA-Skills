## Description:

An out-of-the-box hotel search skill powered by Umy MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudwavego](https://clawhub.ai/user/cloudwavego)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search hotels by location, stay dates, budget, rating, and hotel keywords, with English and Chinese prompt guidance for extracting structured search parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel searches can send precise location, dates, hotel IDs, and query text to Umy.

Mitigation: Avoid entering personal information in hotel queries, and send only structured hotel search parameters needed for the request.

Risk: The included script adds Umy booking links to hotel results.

Mitigation: Review booking links before use and treat generated links as third-party Umy destinations.

Risk: The bundled public API key is rate-limited and shared.

Mitigation: Use a dedicated Umy API key when reliable quota, attribution, or operational isolation is required.

Risk: Server security evidence says the docs understate executable code and travel data handling.

Mitigation: Review the included script and data handling behavior before installing or enabling the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cloudwavego/skills/umy-hotel)
- [Skill manifest](artifact/SKILL.md)
- [English hotel search prompt](artifact/prompts/search-hotels.md)
- [Chinese hotel search prompt](artifact/prompts/search-hotels_zh.md)
- [Umy API key application](https://mcp.umy.com/apply)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and optional JSON API responses from the included CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hotel search parameters include coordinates, check-in and check-out dates, optional hotel keyword, radius, budget, rating, star rating, and currency.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
