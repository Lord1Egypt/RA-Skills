## Description:

Create a pre-restart audit and rollback archive for system-level changes that preserves backups, execution plans, diffs, verification notes, and rollback context before restart-sensitive edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zczcm85](https://clawhub.ai/user/zczcm85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill before high-risk system changes to scaffold audit records, before-state backups, planned after-state evidence, diffs, verification notes, and rollback paths. It is aimed at restart-sensitive changes to configuration, plugins, routing, approvals, startup behavior, services, and other fragile system paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Archive evidence may be overwritten or collide with prior records.

Mitigation: Harden or review the helper before audit-critical use so it creates unique archive directories, refuses collisions, and uses exclusive creation for records and backups.

Risk: User-provided text can be written into operational Markdown records.

Mitigation: Sanitize or constrain Markdown fields before using archive records for operations, audit, or handoff.

Risk: Workspace fallback storage is weaker than a persistent archive root if restart or service failure affects local state.

Mitigation: Prefer an explicit archive root, SYSTEM_CHANGE_ARCHIVE_ROOT, or writable persistent storage, and clearly disclose when fallback storage is used.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zczcm85/skills/system-change-archive)
- [Archive Schema](artifact/references/archive-schema.md)
- [Path Resolution Rules](artifact/references/path-resolution.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown records, JSON metadata, directory scaffolds, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates PRE-RESTART and POST-RESTART archive structures with optional before-state file copies and a daily index.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
