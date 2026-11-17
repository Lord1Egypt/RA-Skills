## Description:

View and modify Codex CLI configuration settings in ~/.cursor/cli-config.json for permissions, approval mode, editor behavior, display options, sandboxing, network settings, and related CLI preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CLI users use this skill when they want an agent to inspect or update Codex CLI preferences, especially security-sensitive settings such as permissions, approval mode, sandboxing, and network access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently alter security-sensitive Codex CLI settings such as approval mode, sandboxing, permissions, and network access.

Mitigation: Review the exact proposed diff before allowing writes, and avoid broad allowlists, Run Everything, disabled sandboxing, or unrestricted network access unless the persistent effect is intended.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configuration changes can persist across future CLI sessions, so proposed edits should be reviewed before writing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
