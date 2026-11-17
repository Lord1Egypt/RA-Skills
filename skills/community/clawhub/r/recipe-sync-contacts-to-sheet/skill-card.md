## Description:

Export Google Contacts directory to a Google Sheets spreadsheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Workspace administrators and operations teams use this recipe to export Google Workspace directory contacts into a Google Sheet for review, reporting, or controlled synchronization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe exports directory contacts, including phone numbers, to a Google Sheet.

Mitigation: Run it only with authorization to export directory contacts, limit exported fields to what is needed, and avoid unnecessary retention or broad sharing of personal contact data.

Risk: The destination Sheet may expose contact data if its sharing permissions are too broad.

Mitigation: Confirm the destination Google Sheet has appropriate sharing permissions before appending contact rows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-sync-contacts-to-sheet)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command-line tool and the gws-people and gws-sheets skills.]

## Skill Version(s):

1.0.12 (source: server release evidence); artifact metadata version 0.22.5

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
