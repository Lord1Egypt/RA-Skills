## Description:

Tinker helps agents control the Tinker desktop toolbox from the command line, including opening plugins, listing running plugins, invoking plugin MCP tools, and integrating Tinker through MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[surunzi](https://clawhub.ai/user/surunzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to operate Tinker plugins from terminal workflows and to route plugin MCP tool calls through the Tinker CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can allow an agent to launch and control the local Tinker desktop app and plugin windows through the tinker CLI.

Mitigation: Install it only where Tinker is intentionally used, review proposed tinker commands before execution, and keep agent command permissions scoped to tinker commands.

Risk: Plugin-provided MCP tools may perform actions based on each installed plugin's permissions.

Mitigation: Review installed Tinker plugins separately before allowing tool invocation, and disable plugins whose capabilities are not needed.

## Reference(s):

- [Tinker website](https://tinker.liriliri.io/)
- [ClawHub skill page](https://clawhub.ai/surunzi/skills/tinker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Tinker desktop app and CLI; plugin-specific output depends on installed Tinker plugins.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
