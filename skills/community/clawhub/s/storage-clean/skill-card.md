## Description:

Scans Windows, macOS, and Linux storage usage, classifies cleanup candidates into three tiers, and generates an interactive HTML report with copyable cleanup commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when a local machine is low on disk space to inventory system, user, and development storage, review large or old files, and decide which cleanup commands to run manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can expose sensitive local file paths and storage inventories.

Mitigation: Treat generated reports as sensitive local files; avoid sharing them unless paths and inventory details have been reviewed or redacted.

Risk: Copy-paste cleanup commands and bundled deletion tooling can remove local files if used on the wrong target.

Mitigation: Review the exact target paths before running cleaner.py or any copied rm, Remove-Item, sudo, or Docker prune command.

Risk: Cleanup suggestions may classify files as safe or confirm-first even when the user still needs them.

Mitigation: Prefer opening and inspecting directories or files first, and keep backups for important user data before deleting anything.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/storage-clean)

## Skill Output:

**Output Type(s):** [Analysis, Files, Shell commands, Guidance]

**Output Format:** [Terminal text plus generated JSON and interactive HTML reports with copyable shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scanner writes local reports under reports/ and does not automatically delete files; generated reports contain detailed local file paths.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
