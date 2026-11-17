## Description:

AI-powered weekly report generator that scans GitHub issues, pull requests, commits, calendar events, reminders, and project files to produce a polished weekly report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fx-world888](https://clawhub.ai/user/fx-world888)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to aggregate weekly work signals from GitHub, calendar, and task sources into a report for weekly summaries, work summaries, or standup updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may access private GitHub activity covered by the configured token.

Mitigation: Use a fine-grained read-only GitHub token limited to required repositories and prefer specifying repositories explicitly with --repos.

Risk: Generated reports may include sensitive work, calendar, task, issue, or pull request details.

Mitigation: Review generated reports before sharing them outside the intended audience.

Risk: HTML reports may render untrusted issue or pull request titles without sufficient escaping.

Mitigation: Avoid opening HTML reports generated from repositories where untrusted users can control issue or pull request titles until HTML escaping is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fx-world888/skills/weekly-report-fx)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Markdown, HTML, Text, Files]

**Output Format:** [Markdown, HTML, or plain text weekly report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports week offset, output format, report style, repository selection, and dry-run options.]

## Skill Version(s):

1.0.0 (source: release metadata, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
