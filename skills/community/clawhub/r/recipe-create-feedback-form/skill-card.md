## Description: <br>
Create a Google Form for feedback and share it via Gmail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operations teams use this recipe to create an event feedback form in Google Forms and send the form link through Gmail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Gmail command can send a form link outside the user's environment. <br>
Mitigation: Verify the active Google account, recipient address, subject, and message body before execution. <br>
Risk: The Google Forms command creates or changes resources in the active Google Workspace account. <br>
Mitigation: Confirm the intended account and form title before running the command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-create-feedback-form) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a Google Forms creation command and a Gmail send command that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata); artifact metadata version 0.22.5 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
