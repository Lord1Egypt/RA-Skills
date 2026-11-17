## Description:

Export a Google Sheets spreadsheet as a CSV file for local backup or processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and productivity users use this skill to guide an agent through exporting a Google Sheets spreadsheet as CSV for local backup or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exporting a spreadsheet as CSV can create a local copy of sensitive Google Sheets data.

Mitigation: Confirm the selected sheet is appropriate to store locally and verify where the gws export output is saved or redirected before retaining or sharing the CSV.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-backup-sheet-as-csv)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the gws CLI and the gws-sheets and gws-drive skills to inspect and export a selected spreadsheet.]

## Skill Version(s):

1.0.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
