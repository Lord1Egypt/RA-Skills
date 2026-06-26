## Description: <br>
List and download all files from a Google Drive folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Google Workspace users use this recipe to list every file in a Google Drive folder, download file media, and export Google Docs as PDFs through the gws CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recipe can download or export the wrong Drive contents if folder IDs, file IDs, account context, or output paths are incorrect. <br>
Mitigation: Verify the active Google account, folder and file IDs, and local destination before running the generated gws commands. <br>
Risk: The skill depends on external tooling and a companion Drive skill. <br>
Mitigation: Install and trust the gws CLI and load the gws-drive skill before executing the recipe. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-bulk-download-folder) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI, the gws-drive skill, valid Google account access, Drive folder IDs, file IDs, and local output filenames.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
