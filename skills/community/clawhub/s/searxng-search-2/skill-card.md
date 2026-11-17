## Description:

Web search using SearXNG instance via MCP. Provides web search capability for agents with configurable SearXNG endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zfanmy](https://clawhub.ai/user/zfanmy)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to add web search through a configured SearXNG endpoint, either through an MCP server or the included shell script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP configuration uses a relative path to mcp-server.py, which can execute the wrong local script.

Mitigation: Change the MCP config to use an absolute path to the packaged mcp-server.py before installation.

Risk: Copying config.json directly into the mcporter config path can overwrite existing MCP configuration.

Mitigation: Merge the searxng server entry into the existing mcporter config instead of replacing the whole file.

Risk: Search queries are sent to the configured SearXNG endpoint, which may be untrusted.

Mitigation: Use a trusted SearXNG endpoint and avoid sensitive searches unless the endpoint is approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zfanmy/skills/searxng-search-2)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Text, Markdown, or JSON search results with configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured SEARXNG_URL endpoint; MCP tool calls accept a query and optional result limit.]

## Skill Version(s):

0.1.2 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
