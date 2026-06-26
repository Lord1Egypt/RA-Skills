## Description: <br>
Enable a Gmail out-of-office auto-reply with a custom message and date range. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and workspace administrators use this recipe to configure a Gmail vacation responder with an out-of-office message, then verify or disable the setting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recipe can enable broad automatic Gmail replies with a hardcoded subject and message. <br>
Mitigation: Edit the subject and body, confirm the Gmail account, and choose contact or domain restrictions before enabling auto-reply. <br>
Risk: The artifact describes a date range, but the shown enable command does not set actual start and end dates. <br>
Mitigation: Add supported start and end date parameters for the gws command, or verify the responder is disabled when the user returns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-create-vacation-responder) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws command and the gws-gmail skill.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
