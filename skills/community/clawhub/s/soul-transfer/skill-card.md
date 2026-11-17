## Description:

Backup and restore an OpenClaw agent's full workspace, including memory, config, credentials, skills, and cron jobs, to or from a Git repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crypticdriver](https://clawhub.ai/user/crypticdriver)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to migrate, back up, restore, and verify OpenClaw agent workspaces across instances or fresh machines. It also supports rebuilding recurring backup cron jobs after restore.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles credentials, channel tokens, API keys, agent instructions, skills, and recurring Git pushes, which could expose secrets or restore unsafe authority.

Mitigation: Review and change the workflow before installing; do not commit plaintext secrets, avoid tokens in Git URLs, restore only from a trusted pinned revision, and review restored skills and instruction files before activation.

Risk: Restoring exec security settings and unattended cron jobs can broaden agent authority or trigger repeated pushes without sufficient review.

Mitigation: Do not restore exec security increases automatically, and disable or narrow recurring cron jobs unless unattended pushes are explicitly desired.

## Reference(s):

- [Cron Job Templates](references/cron-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/crypticdriver/skills/soul-transfer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with shell commands, JSON configuration examples, and a helper shell script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes backup, restore, verification, and cron rebuild procedures.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
