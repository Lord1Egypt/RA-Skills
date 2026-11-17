## Description:

Guidance-only setup skill that helps an agent add 20-second trailing-window debounce behavior to a user's locally installed openclaw-weixin channel plugin after explicit consent and backup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yechang1450](https://clawhub.ai/user/yechang1450)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill when they explicitly want an agent to enable or repair burst-message debouncing for the openclaw-weixin channel. The skill guides local inspection, consent, backup, implementation, restart, verification, reporting, and rollback for the installed plugin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to modify a locally installed openclaw-weixin plugin and restart the gateway.

Mitigation: Proceed only after explicit user consent that names the target path, plugin version, files to change, planned behavior, backup directory, and restart impact; verify backups before editing and provide rollback steps.

Risk: Unsafe approval could permit elevated writes, system-level plugin changes, or dependency installation without a trustworthy lockfile.

Mitigation: Do not approve elevated or system-level modifications; require a user-level plugin location and a reviewable lockfile before any dependency-backed build step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yechang1450/skills/weixin-debounce20s)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and code-edit instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local plugin modification only after explicit consent, backup, deterministic build checks, restart, verification, and rollback reporting.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
