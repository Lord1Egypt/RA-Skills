## Description:

Share a Google Drive folder and all its contents with a list of collaborators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams use this recipe to locate a Google Drive folder, add collaborators with reader or writer permissions, and verify the resulting access list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sharing the wrong folder or granting writer access to unintended collaborators can expose or modify all contents in the selected Google Drive folder.

Mitigation: Confirm the folder ID, collaborator email addresses, and intended roles before running permission commands; verify permissions afterward and revoke unintended access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-share-folder-with-team)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command-line tool and gws-drive skill context.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
