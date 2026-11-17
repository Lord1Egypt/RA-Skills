## Description:

Read event data from a Google Sheets spreadsheet and create Google Calendar entries for each row.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and productivity automation agents use this recipe to read event rows from Google Sheets and create matching Google Calendar entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect sheet ranges or row data may create unwanted calendar events or add attendees.

Mitigation: Review the selected sheet range carefully and test with a small range before running against uncertain sheet contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-create-events-from-sheet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command-line tool and the gws-sheets and gws-calendar skills.]

## Skill Version(s):

1.0.14 (source: server release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
