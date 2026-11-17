## Description:

Upgrades an OpenClaw Gateway installation with release-note review, backup, Node.js compatibility checks, systemd updates, restart health checks, and rollback handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luffertlu](https://clawhub.ai/user/luffertlu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan and execute OpenClaw Gateway upgrades on Linux or WSL2 systems that run OpenClaw from a global npm installation under a user-level systemd service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The updater installs openclaw@latest and can replace the user-level gateway installation and edit the user systemd service.

Mitigation: Review release notes and package source before execution; prefer pinning a confirmed version from a trusted registry with integrity verification.

Risk: A failed restart or incompatible runtime can interrupt the OpenClaw Gateway service.

Mitigation: Confirm Node.js compatibility and systemd user permissions before upgrading, keep the fallback backup available, and inspect the generated logs if rollback is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luffertlu/skills/self-upgrade-gateway)
- [OpenClaw GitHub releases API](https://api.github.com/repos/openclaw/openclaw/releases)
- [OpenClaw npm registry package](https://registry.npmjs.org/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell-command execution steps and status reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke a bundled bash upgrade script that writes logs under the user's OpenClaw workspace.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
