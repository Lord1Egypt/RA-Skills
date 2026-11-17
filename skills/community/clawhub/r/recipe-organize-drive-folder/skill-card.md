## Description:

Create a Google Drive folder structure and move files into the right locations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this recipe to create Google Drive folders, move existing files into the right folders, and verify the resulting folder structure with Google Workspace commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe can persistently reorganize Google Drive contents by creating folders and moving files.

Mitigation: Confirm the file ID, old parent folder ID, and destination folder ID before running move commands, and list affected files first when practical.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-organize-drive-folder)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command-line tool and the gws-drive skill.]

## Skill Version(s):

1.0.12 (source: ClawHub release metadata; skill metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
