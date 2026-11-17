## Description:

Smart File Organizer Pro helps organize local files with mode presets, date-based archiving, progress display, and operation history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shianaixuexi-cell](https://clawhub.ai/user/shianaixuexi-cell)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze and organize local directories by file type, date, and duplicate status. It supports preview, backup, history, and undo workflows for file cleanup and archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move, rename, and sometimes delete many local files.

Mitigation: Run preview mode first, start with a test or backed-up directory, and avoid duplicate deletion unless separate backups exist.

Risk: Custom configuration can change file categories, renaming, duplicate handling, and backup behavior.

Mitigation: Use trusted configuration files only and review settings before executing on important directories.

Risk: Undo and history may not provide complete recovery for every filesystem change.

Mitigation: Keep independent backups and treat built-in undo/history as convenience features rather than full recovery guarantees.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shianaixuexi-cell/skills/smart-file-organizer-pro)
- [Publisher profile](https://clawhub.ai/user/shianaixuexi-cell)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands, terminal text, JSON history, and local report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; helper scripts can move, rename, copy, delete, and restore files in local directories.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-03-12; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
