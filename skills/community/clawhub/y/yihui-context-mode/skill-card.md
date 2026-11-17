## Description:

YiHui CONTEXT MODE helps coding agents conserve context by routing large command, file, and web outputs through context-mode tools for searchable summaries and session continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1yihui](https://clawhub.ai/user/1yihui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers using AI coding agents use this skill to inspect projects, run commands, fetch or index research material, and preserve session continuity while reducing raw tool output in context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server is installed through an unpinned npm invocation and may change between installations.

Mitigation: Pin and review the npm package version before installing or enabling the server.

Risk: The MCP server can execute commands and read or index local content.

Mitigation: Run it with limited filesystem access and avoid indexing private repositories or sensitive files until storage and cleanup behavior are clear.

Risk: The MCP server can fetch web data and place fetched material into searchable context.

Mitigation: Fetch trusted URLs only and review indexed results before acting on generated guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1yihui/skills/yihui-context-mode)
- [Publisher profile](https://clawhub.ai/user/1yihui)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text, Configuration]

**Output Format:** [Markdown with inline shell commands and terse text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use MCP tools to execute commands, fetch web content, and index local or fetched content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
