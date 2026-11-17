## Description:

Initialize and configure OpenClaw agent workspace Markdown files for new or customized agents, including identity, user profile, tools, bootstrap, heartbeat, and operating instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szsip239](https://clawhub.ai/user/szsip239)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to gather setup requirements through an interview and generate concise workspace Markdown files for an agent. It supports both container and host OpenClaw instances and helps preserve existing AGENTS.md infrastructure while adding user-specific configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional uv installer path runs a remote shell script without verification.

Mitigation: Avoid the --install path unless the installer is replaced with a pinned and verified installation method.

Risk: Generated workspace files are injected into future agent prompt context and can affect agent behavior.

Mitigation: Use trusted interview input only and confirm each generated file before writing.

Risk: Updates to AGENTS.md can overwrite important operating instructions if applied carelessly.

Mitigation: Read the existing AGENTS.md first and extend preserved sections instead of replacing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/szsip239/skills/whois)
- [OpenClaw Workspace Guide](references/openclaw-workspace.md)
- [OpenClaw Official Workspace Templates](references/templates.md)
- [uv installer script URL used by optional install path](https://astral.sh/uv/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files with inline shell commands and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates or updates AGENTS.md, SOUL.md, IDENTITY.md, USER.md, TOOLS.md, HEARTBEAT.md, and optionally BOOTSTRAP.md after interview and user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
