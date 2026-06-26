## Description: <br>
Export a Google Sheets spreadsheet as a CSV file for local backup or processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate Google Workspace CLI commands that export a Google Sheets spreadsheet as CSV for backup, migration, or local processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exported CSV files can contain sensitive spreadsheet data. <br>
Mitigation: Verify the spreadsheet ID, selected sheet or range, and local destination before running the export command; handle the resulting CSV as sensitive data. <br>
Risk: The commands require Google Workspace CLI access to Sheets and Drive resources. <br>
Mitigation: Use an account with appropriate permissions, review the generated command before execution, and follow normal installation caution as recommended by the clean ClawScan security guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-backup-sheet-as-csv) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws binary and the gws-sheets and gws-drive skills.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata; artifact metadata version: 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
