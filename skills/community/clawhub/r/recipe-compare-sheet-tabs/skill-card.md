## Description: <br>
Read data from two tabs in a Google Sheet to compare and identify differences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and workspace users use this recipe to read two Google Sheets tabs and compare their rows or cells for changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recipe could read data from an unintended Google account, spreadsheet, or tab range if placeholders are reused without review. <br>
Mitigation: Confirm gws is authenticated to the intended Google account and replace the example spreadsheet ID and tab ranges with only sheets you want read. <br>


## Reference(s): <br>
- [Recipe Compare Sheet Tabs on ClawHub](https://clawhub.ai/googleworkspace-bot/recipe-compare-sheet-tabs) <br>
- [googleworkspace-bot publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and comparison notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws binary and gws-sheets skill; reads only the spreadsheet ID and tab ranges supplied for the task.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
