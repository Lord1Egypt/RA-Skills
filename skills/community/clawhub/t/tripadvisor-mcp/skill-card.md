## Description:

TripAdvisor MCP helps agents look up hotels, restaurants, attractions, place details, photos, and reviews through TripAdvisor Terra API data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to configure an MCP connection that lets an agent search TripAdvisor locations, compare places to stay or eat, and retrieve ratings, reviews, photos, and nearby attractions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running an unpinned external npm package can expose users to unexpected package changes.

Mitigation: Review the referenced npm package or build from source, and pin an exact version before use.

Risk: TripAdvisor API keys may be exposed if MCP configuration files are committed or shared.

Mitigation: Keep API-key-bearing MCP configuration out of version control and use a dedicated, revocable Terra API key with quota limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischall/skills/tripadvisor-mcp)
- [npm package @chrischall/tripadvisor-mcp](https://www.npmjs.com/package/@chrischall/tripadvisor-mcp)
- [TripAdvisor developers](https://www.tripadvisor.com/developers)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TripAdvisor Terra API key and MCP server registration; outputs are read-only travel data lookups.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
