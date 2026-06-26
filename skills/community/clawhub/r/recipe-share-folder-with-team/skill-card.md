## Description: <br>
Share a Google Drive folder and all its contents with a list of collaborators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and workspace operators use this skill to find a Google Drive folder, grant collaborator access, and verify the resulting permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sharing the wrong folder can expose unrelated Google Drive contents. <br>
Mitigation: Verify the active Google account, exact folder ID, and current folder contents before creating permissions. <br>
Risk: Incorrect recipient addresses or overly broad editor access can grant unintended access. <br>
Mitigation: Confirm each email address and grant writer access only to collaborators who need to modify files. <br>
Risk: Folder permissions may remain active after the immediate collaboration need ends. <br>
Mitigation: Review the permissions list after sharing and remove access when it is no longer required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-share-folder-with-team) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws command and the gws-drive skill.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; skill metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
