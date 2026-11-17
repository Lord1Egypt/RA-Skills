## Description:

Packages, migrates, and clones OpenClaw agent team configurations, preserving identity files, team members, skills, scheduled tasks, and agent configuration with review controls before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhao-zwl](https://clawhub.ai/user/zhao-zwl)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and agent developers use this skill to back up, move, restore, or duplicate an agent team across environments. It helps package and reapply workspaces, identity files, team member data, skills, scheduled tasks, and agent configuration while offering dry-run and skip controls for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The migration workflow can overwrite active agent state, install skills, create scheduled tasks, and write broadly under the OpenClaw profile.

Mitigation: Use only trusted migration packages, inspect package contents first, run dry-run before restoring, and keep the automatic backups available for rollback.

Risk: Migration packages may include sensitive memory and tool configuration files such as MEMORY.md and TOOLS.md.

Mitigation: Do not share migration archives publicly; store and transfer them with encryption or another trusted channel.

Risk: Scheduled tasks can run agent payloads automatically after migration.

Mitigation: Review every cron payload before enabling tasks and start with --no-cron when restoring into an active profile.

Risk: Gateway restarts can interrupt active sessions and running work.

Mitigation: Use --no-restart during staged validation and restart manually after confirming the restored configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhao-zwl/skills/team-resurrection)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Material packing guide](artifact/MATERIAL_PACKING.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands and generated ZIP/configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the openclaw CLI; workflows can write OpenClaw profile files, install scheduled tasks, and restart the gateway.]

## Skill Version(s):

1.1.2 (source: server release metadata and SKILL.md openclaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
