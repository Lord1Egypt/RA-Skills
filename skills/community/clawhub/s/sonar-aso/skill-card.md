## Description:

Sonar ASO gives agents App Store Optimization data via the Sonar API, including keyword metrics, app lookup and search, ASO audits, review mining, and revenue estimates for iOS and Android apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[petersutarik](https://clawhub.ai/user/petersutarik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, app marketers, and agents use this skill to research app-store keywords, compare competitor apps, audit ASO metadata, mine user reviews, and estimate app revenue for iOS and Android markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using an unpinned npm MCP package can execute changing third-party code.

Mitigation: Prefer direct Sonar API calls or a pinned, reviewed MCP server version.

Risk: The Sonar API key could be exposed alongside unrelated credentials in an agent or MCP server environment.

Mitigation: Run the MCP server with only SONAR_API_KEY in scope and avoid passing unrelated credentials.

## Reference(s):

- [Sonar homepage](https://trysonar.app)
- [Sonar developer access](https://trysonar.app/developers)
- [Sonar MCP documentation](https://trysonar.app/docs/mcp)
- [Sonar API documentation](https://trysonar.app/docs/api)
- [ClawHub skill page](https://clawhub.ai/petersutarik/skills/sonar-aso)
- [Publisher profile](https://clawhub.ai/user/petersutarik)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with API examples and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SONAR_API_KEY for Sonar API access; API responses are JSON envelopes and include credit usage headers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
