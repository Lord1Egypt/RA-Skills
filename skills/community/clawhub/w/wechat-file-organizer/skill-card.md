## Description:

Scans locally received WeChat files, organizes them by type or month, finds duplicates, and creates JSON or standalone HTML reports with optional custom sorting rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

Individual WeChat users can review, sort, and deduplicate locally received files, apply custom matching rules, and create machine-readable or visual reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because cleanup may permanently remove originals despite recovery assurances; the scan is partial, so the evidence is incomplete.

Mitigation: Review the cleanup behavior, keep backups, and verify recovery behavior for the operating system and storage volume before using --apply --trash; start with the default dry run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oracis/skills/wechat-file-organizer)
- [Project homepage (listed in the artifact manifest)](https://github.com/oracis/wechat-file-organizer)

## Skill Output:

**Output Type(s):** [File organization, JSON, HTML reports, Guidance]

**Output Format:** [Organized local files, JSON summaries, and standalone HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local processing; defaults to a read-only dry run, with explicit options for copying, deduplication, and moving originals to the system trash.]

## Skill Version(s):

2.3.0 (source: SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
