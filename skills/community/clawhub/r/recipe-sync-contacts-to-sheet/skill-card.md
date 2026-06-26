## Description: <br>
Export Google Contacts directory to a Google Sheets spreadsheet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and workspace administrators use this recipe to export Google Workspace directory contact names, email addresses, and phone numbers into a Google Sheet for authorized productivity workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Organization directory contact data could be exported without proper authorization or shared too broadly in the destination Sheet. <br>
Mitigation: Confirm authorization, run gws under the intended Google account, restrict Sheet access, and remove or limit exported data when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-sync-contacts-to-sheet) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws binary and the gws-people and gws-sheets skills.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; skill metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
