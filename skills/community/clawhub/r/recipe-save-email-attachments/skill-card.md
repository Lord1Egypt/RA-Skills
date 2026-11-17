## Description:

Find Gmail messages with attachments and save them to a Google Drive folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workspace users use this recipe to find selected Gmail messages with attachments, download the attachments, and upload them to an approved Google Drive folder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe can access Gmail attachments and copy them into Google Drive.

Mitigation: Use a narrow Gmail query, confirm each attachment before retaining it, and upload only to an approved Drive folder with appropriate sharing controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-save-email-attachments)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI plus gws-gmail and gws-drive skills.]

## Skill Version(s):

1.0.12 (source: server release metadata); artifact metadata version 0.22.5

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
