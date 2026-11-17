## Description:

A safety net for AI agents. Catches unsafe tool calls before they execute.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devlines](https://clawhub.ai/user/devlines)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Yabbie Net to route MCP tool calls through a safety proxy that can block unsafe actions before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A third-party npm proxy sits in the path of MCP tool calls and can block or delay tool execution.

Mitigation: Review the package before deployment, run it with least privilege, and wrap only MCP servers whose calls you are comfortable routing through the proxy.

Risk: Unpinned npx execution examples can install or run unexpected package versions.

Mitigation: Pin npm package versions before installation and prefer a project dependency over global installation.

Risk: Optional tier2 judging or telemetry can introduce additional data flows when intentionally enabled.

Mitigation: Keep tier2 and telemetry disabled unless those flows are intended, and review the configured provider and transmitted summaries before enabling them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devlines/skills/yabbie-net)
- [Publisher profile](https://clawhub.ai/user/devlines)
- [Homepage](https://yabbie.net)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup guidance for npm installation, MCP server wrapping, yabbie.yaml configuration, audit commands, and operational cautions.]

## Skill Version(s):

0.2.0 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
