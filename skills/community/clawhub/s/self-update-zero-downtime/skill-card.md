## Description:

Guides OpenClaw upgrades by checking release information and Node.js compatibility, creating a backup, installing the update, and checking or rolling back the service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luffertlu](https://clawhub.ai/user/luffertlu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to plan and carry out an OpenClaw upgrade on a supported Linux installation, including compatibility checks and service recovery steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Upgrade or rollback steps can delete or replace files before they are safely validated or approved.

Mitigation: Review the commands before execution, confirm the target version, and verify that a recoverable backup exists before allowing installation or rollback steps to change files.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/luffertlu/skills/self-update-zero-downtime)
- [OpenClaw GitHub releases](https://github.com/openclaw/openclaw/releases)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Step-by-step upgrade guidance and a Bash script for supported installations.]

## Skill Version(s):

1.1.0 (source: evidence.json release.version, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
