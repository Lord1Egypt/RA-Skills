## Description: <br>
Append a deal status update to a Google Sheets sales tracking spreadsheet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and operations users can use this recipe to find a Google Sheets sales pipeline, inspect the current data, and append a new deal status row through Google Workspace commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recipe uses the active Google Workspace account to read a sales pipeline spreadsheet and append a row. <br>
Mitigation: Verify the active gws account and confirm the target spreadsheet ID before running the append command. <br>
Risk: The example row contains placeholder deal data that could be written to a real tracking sheet if reused as-is. <br>
Mitigation: Replace the example date, account, status, amount, quarter, and owner values with the intended deal update before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-log-deal-update) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws command and the gws-sheets and gws-drive skills. Uses the active Google Workspace account to read and append spreadsheet rows.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
