## Description:

Checks QwenPaw MCP configuration and server connectivity, then suggests fixes for common connection and configuration problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trend0522](https://clawhub.ai/user/trend0522)

### License/Terms of Use:

MIT-0

## Use Case:

QwenPaw users and developers use this skill to inspect MCP configuration, check configured server connections, and troubleshoot authentication, timeout, or tool-name conflicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reading local MCP configuration may display sensitive connection details.

Mitigation: Review and redact configuration details before sharing the diagnostic report.

Risk: Connection probes may contact private or sensitive configured MCP servers.

Mitigation: Review configured endpoints before running connection checks.

## Reference(s):

- [QwenPaw MCP Helper on ClawHub](https://clawhub.ai/trend0522/skills/qwenpaw-mcp-helper)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown diagnostic report with issues, suggestions, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports configuration validity and server connection counts; requires qwenpaw, python3, and curl.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
