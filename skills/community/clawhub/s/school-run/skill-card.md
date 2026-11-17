## Description:

Manages the School Run Schedule Google Sheet for reading or updating the drop-off schedule for Damian and Zachary, including date, responsible person, and marks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cbasah](https://clawhub.ai/user/cbasah)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or household operators use this skill to inspect and update a specific school-run Google Sheet schedule. It helps an agent prepare Google Workspace CLI reads and dry-run-first updates for dates, drop-off responsibility, and marks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify a live school-run schedule.

Mitigation: Require the agent to show the sheet tab, range, old value, and new value before any update, and perform a dry run before writes.

Risk: The skill references a hardcoded service-account credential path.

Mitigation: Use it only when authorized to manage the spreadsheet, and scope the service account only to the referenced spreadsheet.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Google Workspace CLI commands against a specific Google Sheet and asks for dry-run review before writes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
