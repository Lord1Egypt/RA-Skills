## Description:

Backs up configured Mac workspace folders to a fixed local folder and an external drive with incremental copying, verification, and resumable runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentjiang06](https://clawhub.ai/user/vincentjiang06)

### License/Terms of Use:

MIT-0

## Use Case:

Mac users and developers use this skill to plan, run, verify, and check the status of local workspace backups across configured destinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The backup can read and copy sensitive files in configured workspace folders.

Mitigation: Review configured source roots and destinations before the first write; expand secret patterns for sensitive files such as id_rsa, credentials.json, and .npmrc.

Risk: A destination that syncs off-machine could disclose copied files.

Mitigation: Review destination locations and require explicit owner approval before enabling off-machine copying or acknowledging secrets.

Risk: The documented case-only duplicate source-root edge case can undermine backup coverage.

Mitigation: Avoid source roots differing only by letter case until the issue is fixed, and confirm backup coverage in the status report.

## Reference(s):

- [ClawHub workspace-backup release](https://clawhub.ai/vincentjiang06/skills/workspace-backup)
- [First-run setup](references/first-run-setup.md)
- [Destination policy](references/destination-policy.md)
- [Backup ledger format](references/ledger-format.md)
- [Rsync compatibility](references/openrsync-compat.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown status reports and backup guidance, with commands and optional JSON status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; reports distinguish planned copies from verified backups.]

## Skill Version(s):

0.3.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
