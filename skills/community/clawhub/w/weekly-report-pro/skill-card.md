## Description:

Weekly Report Pro collects local Git commit history, optional code statistics, Markdown checklist progress, and user-provided work notes to draft structured weekly or monthly work reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangbinbinm](https://clawhub.ai/user/tangbinbinm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical leads, and other professionals use this skill to turn local repository activity, task completion data, and concise status notes into results-oriented weekly or monthly reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read Git commit metadata from directories selected by the user and may include sensitive project or author information in generated report material.

Mitigation: Point the collection command at specific project folders and review the generated report before sharing it.

Risk: If a Markdown plan file is provided, task names and completion status from that local file may be summarized in the report.

Mitigation: Use only intended plan files and remove private task details from the generated report before distribution.

## Reference(s):

- [Weekly Report Pro README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/tangbinbinm/skills/weekly-report-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports with optional shell commands for local Git data collection and JSON-derived metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports weekly and monthly report modes, Chinese or English report templates, role-specific framing, and optional dashboard and goal-tracking metrics.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
