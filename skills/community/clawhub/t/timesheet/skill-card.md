## Description:

Track time, manage projects and tasks using timesheet.io CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[florianrauscha](https://clawhub.ai/user/florianrauscha)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate the timesheet.io CLI for authenticated time tracking, project and task management, timer control, tags, reports, and exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to use an authenticated timesheet.io CLI session or API key.

Mitigation: Install and invoke it only when the agent is intended to access the user's timesheet.io account, and avoid exposing TIMESHEET_API_KEY in shared logs or transcripts.

Risk: The documented CLI workflows include delete commands for projects, tasks, and tags.

Mitigation: Review target IDs and names before approving delete operations.

Risk: Report export commands can produce CSV or XLSX files containing sensitive business, billing, or work-history data.

Mitigation: Treat exported reports as sensitive files and share or store them according to the user's data-handling requirements.

## Reference(s):

- [timesheet.io](https://timesheet.io)
- [ClawHub skill page](https://clawhub.ai/florianrauscha/skills/timesheet)
- [Publisher profile](https://clawhub.ai/user/florianrauscha)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, Files]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the timesheet CLI and authenticated timesheet.io access; exported reports may contain sensitive business or billing data.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
