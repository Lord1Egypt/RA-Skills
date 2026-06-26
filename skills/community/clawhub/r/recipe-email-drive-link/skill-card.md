## Description: <br>
Share a Google Drive file and email the link with a message to recipients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operators use this skill to share a specific Google Drive file with a recipient and send an email containing the file link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Google Drive file link or permission could be sent to the wrong recipient or created with the wrong role. <br>
Mitigation: Before running the recipe, verify the active Google account, file, recipient address, permission role, subject, and body; revoke the Drive permission if it was created by mistake. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-email-drive-link) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Google Workspace CLI and the gws-drive and gws-gmail skills.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
