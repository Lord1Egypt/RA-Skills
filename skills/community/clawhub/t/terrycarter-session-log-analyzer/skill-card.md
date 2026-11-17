## Description:

View and analyze session logs, generate PDF reports, and sync to Notion. Supports daily automated reporting via cron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect agent session logs, summarize operational activity, generate reports, and optionally sync those reports to Notion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The daily cron workflow can repeatedly process session logs and upload generated reports to Notion without interactive review.

Mitigation: Enable scheduled reporting only after reviewing the logs that may be processed, confirming the target Notion database, and documenting how to inspect and remove the crontab entry.

Risk: Session logs may contain sensitive operational details before reports are synced externally.

Mitigation: Review or redact logs before syncing reports, and run the workflow under an unprivileged account with only the required Notion access.

Risk: The workflow depends on Python packages and another skill to generate and sync reports.

Mitigation: Pin and audit dependencies where possible before installing or enabling unattended execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/terrycarter-session-log-analyzer)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate PDF reports and trigger Notion API uploads when the documented workflow is configured.]

## Skill Version(s):

1.2.1 (source: release evidence, artifact frontmatter, artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
