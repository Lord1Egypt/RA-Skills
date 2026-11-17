## Description:

Provides smart restart protection for OpenClaw Gateway to prevent restart loops, control restart frequency, preserve state, and support safe recovery after configuration changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackytianjp](https://clawhub.ai/user/jackytianjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to restart OpenClaw Gateway with rate limits, lock checks, configuration backups, health checks, and status reporting. It is intended for managing local OpenClaw Gateway recovery while reducing the chance of runaway restart loops or concurrent restart conflicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can stop and start OpenClaw Gateway.

Mitigation: Install it only when the operator intends to grant restart authority, and review restart actions before deployment.

Risk: The skill creates persistent local backups of OpenClaw configuration.

Mitigation: Review backup contents, storage location, and file permissions so sensitive configuration is not exposed.

Risk: The security guidance calls out /tmp lock-file handling as a production concern.

Mitigation: Fix or review the lock-file handling before production use and avoid running the skill as a privileged user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackytianjp/skills/smart-restart-protection)
- [Artifact README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, shell command output, JavaScript API results, JSON reports, and markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local restart records, logs, configuration backups, and status reports under the user's OpenClaw directories.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
