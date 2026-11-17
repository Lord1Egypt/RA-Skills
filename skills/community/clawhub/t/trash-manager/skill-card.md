## Description:

Trash management with index tracking for all agents. Use when deleting files to ensure proper index registration and 7-day auto-cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucas260514](https://clawhub.ai/user/lucas260514)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to replace direct file deletion with a tracked trash workflow that supports listing, restoration, and scheduled cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill redirects deletion workflows to an unbundled local trash-manager.sh script.

Mitigation: Review and trust the local script source, permissions, allowed paths, and restore behavior before enabling the skill.

Risk: The recommended cleanup can permanently remove trashed files after the retention window.

Mitigation: Confirm the 7-day retention policy and cron cleanup settings before installation, and verify restoration behavior before relying on automatic cleanup.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lucas260514/skills/trash-manager)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to use a local trash-manager.sh script, shared index.json tracking, restore commands, and 7-day cleanup behavior.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
