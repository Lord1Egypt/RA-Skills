## Description:

Provides UK police data queries for crime records, police forces, neighbourhood information, and stop-and-search data through a configured API service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to route natural-language UK police-data questions to tools for crime, outcome, force, neighbourhood, and stop-and-search lookups. It requires a XiaoBenYang API key before making queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Police-data queries and the XiaoBenYang API key are sent to the XiaoBenYang MCP backend.

Mitigation: Install only when this data flow is intended, and avoid entering valuable or reusable credentials unless the publisher explains the service relationship.

Risk: The skill stores the API key in a local .env file.

Mitigation: Use a limited-scope key where possible and replace plaintext local storage with safer secret handling before production use.

Risk: Project remnants refer to an unrelated Gaokao configuration, which may make behavior harder to review.

Mitigation: Review the code and tool mapping before deployment, with special attention to endpoint, MCP ID, and credential handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/uk-police-data-query)
- [XiaoBenYang API key page](https://xiaobenyang.com)
- [XiaoBenYang MCP backend](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown summaries of JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success status, raw API response data, and a status message from each tool call.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
