## Description:

Create a Google Shared Drive and add members with appropriate roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Workspace administrators and automation agents use this recipe to create a Google Shared Drive, add a user with the selected role, and verify membership using the Google Workspace CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The commands create persistent Google Workspace resources and permissions.

Mitigation: Review the drive name, requestId, fileId, role, and member email address before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-create-shared-drive)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require the gws CLI and the gws-drive prerequisite skill.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
