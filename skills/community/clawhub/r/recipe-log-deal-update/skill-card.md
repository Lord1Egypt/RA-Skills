## Description:

Append a deal status update to a Google Sheets sales tracking spreadsheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Sales operations users and agents use this recipe to locate a Sales Pipeline spreadsheet, read the Pipeline tab, and append a deal status update row.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The append command can change the wrong Google Sheets sales pipeline if the target spreadsheet or tab is misidentified.

Mitigation: Confirm the Sales Pipeline spreadsheet ID and Pipeline tab before appending any row.

Risk: The example row can create duplicate or mistaken deal entries if used without review.

Mitigation: Read the current sheet first and replace the example row with the actual deal values before running the append step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-log-deal-update)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown recipe steps with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command line tool plus gws-sheets and gws-drive skills; the append step changes a Google Sheets spreadsheet.]

## Skill Version(s):

1.0.12 (source: server release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
