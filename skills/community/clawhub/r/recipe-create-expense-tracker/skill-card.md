## Description:

Set up a Google Sheets spreadsheet for tracking expenses with headers and initial entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workspace users use this skill to create a Google Sheets expense tracker with column headers and an initial sample expense entry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe shares the created spreadsheet with manager@company.com, which could expose expense data to an unintended recipient.

Mitigation: Remove the sharing step or replace the recipient with an explicitly approved email address before running the command.

Risk: The recipe issues Google Workspace commands that create and modify cloud resources.

Mitigation: Review the target spreadsheet name, values, and permissions before execution, and run the commands only in the intended Google Workspace account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-create-expense-tracker)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown recipe with ordered steps and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command-line tool and the gws-sheets and gws-drive skills.]

## Skill Version(s):

1.0.13 (source: server release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
