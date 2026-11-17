## Description:

Read GitHub helps agents access repository documentation and code through gitmcp.io instead of raw GitHub scraping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[am-will](https://clawhub.ai/user/am-will)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to inspect GitHub repositories, fetch documentation, search docs and code, and retrieve referenced URLs through the GitMCP MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs unpinned npm package code through mcp-remote.

Mitigation: Use a restricted environment and pin or pre-approve mcp-remote before installation or execution.

Risk: The skill uses outbound network access and can fetch repository documentation, code search results, and referenced URLs.

Mitigation: Limit network egress to expected services, allowlist trusted repositories and URLs where possible, and avoid passing secrets in repository names, queries, tool arguments, or fetched URLs.

Risk: The direct MCP tool-call path can expose broader remote behavior than the main documentation and search workflow requires.

Mitigation: Prefer the documented fetch and search commands, and remove or allowlist direct MCP tool calls before use in less restricted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/am-will/skills/read-github)
- [GitMCP service](https://gitmcp.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown and plain text responses with optional shell commands and JSON-formatted MCP results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch repository documentation, code search results, and referenced URL content through a remote MCP service.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
