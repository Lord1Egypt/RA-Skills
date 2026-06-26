## Description: <br>
Create a Google Meet meeting space and share the join link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and workspace operators use this recipe to create a Google Meet space and send the meeting link by email through Google Workspace tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recipe creates a Google Meet space with OPEN meeting access. <br>
Mitigation: Review and edit the meeting access configuration before running the command, and use an access policy that matches the organization and meeting audience. <br>
Risk: The recipe sends the meeting link to the fixed address team@company.com. <br>
Mitigation: Confirm or replace the recipient and message content before running the Gmail send step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-create-meet-space) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and the gws-meet and gws-gmail skills.] <br>

## Skill Version(s): <br>
1.0.12 (source: release evidence; skill metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
