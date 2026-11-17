## Description:

Helps an agent perform a zero-downtime OpenClaw self-upgrade using release-note review, backup, npm installation, restart health checks, and rollback handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luffertlu](https://clawhub.ai/user/luffertlu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when they want an agent to check and apply an OpenClaw runtime upgrade while preserving service availability. It is intended for npm-global OpenClaw installations with systemd user services, backup, health-check, and rollback workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify the local OpenClaw runtime and installed service during a real self-upgrade.

Mitigation: Require explicit manual approval before execution, confirm release notes, and pin the exact OpenClaw version and npm registry before installing.

Risk: The security evidence reports that the script can modify the installed service without the user-confirmation gate promised in the instructions.

Mitigation: Treat approval as a required external control and review the generated command sequence before allowing the upgrade script to run.

Risk: Rollback restores service availability but does not protect against a compromised npm package.

Mitigation: Use trusted registry settings, verify the package/version before install, and treat rollback only as availability recovery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luffertlu/skills/self-update-zero-downtime)
- [Publisher Profile](https://clawhub.ai/user/luffertlu)
- [npm registry](https://registry.npmjs.org)
- [OpenClaw GitHub releases API](https://api.github.com/repos/openclaw/openclaw/releases)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and operational status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write upgrade logs to disk and propose or run service-management commands during the upgrade workflow.]

## Skill Version(s):

1.0.3 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
