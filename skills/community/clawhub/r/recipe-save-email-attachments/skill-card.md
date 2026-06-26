## Description: <br>
Find Gmail messages with attachments and save them to a Google Drive folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Google Workspace users and automation agents use this recipe to find selected Gmail messages with attachments, download the relevant files, and upload them to a chosen Google Drive folder. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The recipe accesses Gmail attachments and Google Drive folders, which can expose private or sensitive data if run against the wrong account, query, source message, or folder. <br>
Mitigation: Confirm the Google account, keep the Gmail search query narrow, review the attachment source, and upload only to a Drive folder with appropriate sharing permissions. <br>
Risk: The workflow depends on the gws tooling and companion Gmail and Drive skills. <br>
Mitigation: Install and run the recipe only in environments where those tools and companion skills are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/recipe-save-email-attachments) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws command-line tool and companion Gmail and Drive skills.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; skill metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
