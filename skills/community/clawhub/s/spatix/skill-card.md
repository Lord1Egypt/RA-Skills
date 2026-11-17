## Description:

Spatix helps agents create shareable maps, geocode addresses, visualize GeoJSON or CSV data, search places, and build map URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alde1022](https://clawhub.ai/user/alde1022)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to create maps, geocode locations, visualize spatial datasets, search places, and configure optional Spatix MCP access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location prompts, coordinates, routes, addresses, uploaded datasets, and map titles may be sent to Spatix services.

Mitigation: Review location data before use and avoid sending sensitive, regulated, or unnecessary personal location information.

Risk: Leaderboard attribution can expose agent identifiers publicly.

Mitigation: Use pseudonymous agent_id and agent_name values when enabling attribution.

Risk: The optional MCP server install may run an unpinned package version with access to local files or secrets.

Mitigation: Pin and review the spatix-mcp version, then run it with limited file and secret access.

## Reference(s):

- [Spatix Website](https://spatix.io)
- [Spatix API Docs](https://api.spatix.io/docs)
- [Spatix MCP Server](https://pypi.org/project/spatix-mcp/)
- [ClawHub Skill Page](https://clawhub.ai/alde1022/skills/spatix)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request bodies, map URLs, embed snippets, and MCP configuration.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
