## Description:

Provides agent tools to fetch RFC documents, search RFCs by keyword, and retrieve specific RFC sections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve, search, and summarize RFC material through the provided RFC tool functions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a XiaoBenYang API key and stores it in a local plaintext .env file.

Mitigation: Use a scoped key where possible, avoid shared environments, and remove the .env value when the skill is no longer needed.

Risk: RFC queries are routed through mcp.xiaobenyang.com rather than directly to IETF sources.

Mitigation: Review whether routing through this third-party service is acceptable before sending sensitive or proprietary queries.

Risk: The server security summary flags unrelated gaokao or school-search artifacts in the release.

Mitigation: Inspect the skill package before deployment and prefer a version that removes unrelated artifacts and clearly documents the proxy behavior.

## Reference(s):

- [XiaoBenYang API key provider](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)
- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/rfc-doc)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, Configuration]

**Output Format:** [Markdown or text summaries derived from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a third-party API key before tool calls can succeed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
