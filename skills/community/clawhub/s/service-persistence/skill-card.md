## Description:

Helps developers manage macOS LaunchAgent, tmux bootstrap, and wrapper daemon patterns so services can recover after reboot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darwin7381](https://clawhub.ai/user/darwin7381)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add, migrate, diagnose, and recover persistent macOS services across LaunchAgent and tmux-based tiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create user-level macOS autorun services that restart processes after reboot or failure.

Mitigation: Review generated LaunchAgent, bootstrap, and wrapper changes before loading them, and document how to unload each LaunchAgent and stop related tmux sessions.

Risk: The included behavior references a persistent remote Claude/Telegram agent with bypassed approvals and automatic trust confirmation.

Mitigation: Remove permission-bypass flags, disable automatic trust confirmation, and restrict Telegram or channel access before use.

Risk: Registry-driven service entries can launch arbitrary commands or expose development services beyond the local machine.

Mitigation: Validate registry values before generating scripts and prefer localhost bindings for development services.

## Reference(s):

- [LaunchAgent plist template](references/launchagent-template.md)
- [Bootstrap script template](references/bootstrap-template.md)
- [Service registry specification](references/registry-spec.md)
- [Wrapper daemon script template](references/wrapper-template.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown instructions with inline shell commands and plist, JSON, and shell script templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose macOS LaunchAgent plist files, tmux session commands, service registry JSON updates, and shell scripts.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
