## Description:

List and download all files from a Google Drive folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this recipe to list a Google Drive folder's contents and download each file locally, including exporting Google Docs as PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe downloads Google Drive folder contents to local storage, which may include sensitive files or unexpected filename collisions.

Mitigation: Run it only on folders you are authorized to access, choose a dedicated output directory, review the file list first, and watch for sensitive files or filename collisions.

## Reference(s):

- [Recipe Bulk Download Folder release page](https://clawhub.ai/googleworkspace-bot/skills/recipe-bulk-download-folder)
- [googleworkspace-bot publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require gws and the gws-drive skill, and they may write downloaded Drive files to local storage.]

## Skill Version(s):

1.0.12 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
