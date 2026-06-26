## Description: <br>
Create a Google Drive folder structure and move files into the right locations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this recipe to create Google Drive project folders, add subfolders, move existing files into the right locations, and verify the resulting folder structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recipe can move Google Drive files into different folders. <br>
Mitigation: Confirm the active gws account, list the affected files, and verify FILE_ID, FOLDER_ID, and OLD_PARENT_ID values before running move commands. <br>
Risk: A mistaken parent folder ID can create or verify the folder structure in the wrong Drive location. <br>
Mitigation: Check the intended parent folder and verify the final structure with a Drive file listing after changes. <br>


## Reference(s): <br>
- [Recipe Organize Drive Folder on ClawHub](https://clawhub.ai/googleworkspace-bot/recipe-organize-drive-folder) <br>
- [googleworkspace-bot publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON command parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws binary and the gws-drive skill.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
