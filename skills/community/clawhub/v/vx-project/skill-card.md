## Description:

Guides agents through vx project setup, tool version management, and project configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this guide to initialize vx projects, configure tool versions and scripts, and maintain reproducible development environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following setup guidance may install development tools or change vx.toml and vx.lock.

Mitigation: Review proposed installations and configuration changes before applying or committing them.

Risk: Project hooks and optional AI skill metadata can change repository behavior or write under ~/.vx.

Mitigation: Review hook commands before running setup in sensitive repositories and approve optional metadata writes.

## Reference(s):

- [vx-project on ClawHub](https://clawhub.ai/loonghao/skills/vx-project)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands and TOML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions may include vx.toml, vx.lock, justfile, and project hook examples.]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
