## Description:

Declutter a workspace: enumerate by category (OS residue, stale heartbeats, backups, empty dirs, migration residue), verify consumers per category, remove via recoverable gio trash, and report before/after counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyunlai](https://clawhub.ai/user/zuoyunlai)

### License/Terms of Use:

MIT

## Use Case:

Workspace owners and developers use this skill to identify workspace residue, check whether candidate files and directories are still needed, and carry out recoverable cleanup. It produces categorized findings and a report that distinguishes completed actions, pending decisions, and items retained with reasons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup guidance includes permanent removal of empty directories, which could remove useful workspace structure.

Mitigation: Review each empty directory's ownership and structural role, and check for consumers before removal; retain items whose purpose is unclear.

Risk: The security scan is partial and does not cover some referenced paths.

Mitigation: Review the referenced files that were not included in the scan, along with the cleanup instructions, before installing or using the skill.

## Reference(s):

- [Workspace Declutter on ClawHub](https://clawhub.ai/zuoyunlai/skills/workspace-declutter)
- [Redundancy Categories and Retention List](artifact/references/冗余分类与保留清单.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Categorized Markdown inventory and cleanup report with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports item counts, proposed or completed disposition, before-and-after counts, and items intentionally retained with reasons.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
