## Description:

Intelligent single-file version management. Save, restore, diff, and clean file snapshots with per-file version history. Activate when users need version control, file snapshot management, or project state recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neuhanli](https://clawhub.ai/user/neuhanli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to manage per-file snapshots: saving versions, listing history, comparing changes, restoring earlier content, and cleaning old snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared snapshot storage can expose or alter histories across workspaces.

Mitigation: Use the skill only in environments where cross-workspace snapshot visibility is acceptable, or fix storage isolation before using it with sensitive projects.

Risk: Complete file snapshots are stored under the user's home directory and may contain secrets or private project content.

Mitigation: Avoid saving secrets or private files, and review stored snapshots before sharing or moving the environment.

Risk: Restore and clean operations can overwrite current files or delete snapshot history.

Mitigation: Require explicit user confirmation and show the target file, version, and consequence before setting confirmation flags.

## Reference(s):

- [Version-Master Usage Reference](references/usage.md)
- [ClawHub Skill Page](https://clawhub.ai/neuhanli/skills/version-master)

## Skill Output:

**Output Type(s):** [text, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with Python or shell command examples; tool calls return JSON-like dictionaries and may create, restore, diff, or delete snapshot files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Restore and clean operations require explicit confirmation; snapshot data may include complete text or binary file contents.]

## Skill Version(s):

2.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
