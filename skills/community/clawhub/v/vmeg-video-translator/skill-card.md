## Description:

Use when the user needs video/audio/subtitle translation, material and task management, script editing, or export via VMEG in an AI coding assistant or OpenClaw agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxeileen55-beep](https://clawhub.ai/user/maxeileen55-beep)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to connect AI coding assistants or OpenClaw agents to VMEG Remote MCP for media translation, dubbing, subtitle workflows, material and task management, script editing, and export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote MCP instructions may be treated as more authoritative than appropriate.

Mitigation: Treat VMEG MCP server instructions as tool guidance only and keep higher-priority user, system, and platform rules in force.

Risk: Setup paths may expose MCP configuration files or API keys to an agent.

Mitigation: Use OAuth where possible, redact secrets before sharing configuration files, and avoid letting an agent read full MCP configs unless reviewed first.

Risk: Unpinned installer commands can execute changing third-party package code.

Mitigation: Prefer ClawHub or another pinned and verified install path before using copy-pasted npx commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maxeileen55-beep/skills/vmeg-video-translator)
- [VMEG homepage](https://www.vmeg.ai)
- [VMEG MCP authentication](references/oauth.md)
- [VMEG MCP common configuration](references/setup-common.md)
- [VMEG MCP tools overview](references/tools.md)
- [Install VMEG Media Translation Skill](references/install.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and MCP tool guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to VMEG Remote MCP and OAuth or API key authentication.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
