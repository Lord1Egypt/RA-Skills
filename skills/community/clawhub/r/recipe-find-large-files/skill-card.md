## Description: <br>
Identify large Google Drive files consuming storage quota. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Google Workspace users and administrators use this recipe to list the largest Google Drive files and decide which files to archive or move to reduce storage usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Google Drive listing may reveal private file names, file sizes, MIME types, and owner information. <br>
Mitigation: Run it only in the intended authenticated Google Drive account and avoid sharing command output outside approved audiences. <br>
Risk: The recipe depends on the external gws CLI and gws-drive skill being trusted and authenticated correctly. <br>
Mitigation: Confirm the installed gws binary and gws-drive skill are trusted before using the recipe. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-find-large-files) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Lists Google Drive files sorted by storage quota use; the command is read-only but may expose private file names and owner information.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
