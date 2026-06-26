## Description: <br>
Read data from a Google Sheet and create a formatted Google Docs report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operations users use this recipe to read rows from a Google Sheet, create a Google Docs report, write a formatted summary, and optionally share it with stakeholders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recipe includes a Google Drive permission command with a hard-coded email address, which could share the generated report with an unintended recipient. <br>
Mitigation: Review and edit the sharing step before use; confirm the connected Google account, spreadsheet ID, document ID, and recipient, and keep the document private unless sharing is explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-generate-report-from-sheet) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gws plus the gws-sheets, gws-docs, and gws-drive skills; review the sharing recipient before execution.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
