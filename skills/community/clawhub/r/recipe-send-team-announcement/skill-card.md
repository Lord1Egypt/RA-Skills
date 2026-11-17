## Description:

Send a team announcement via both Gmail and a Google Chat space.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workspace administrators use this recipe to broadcast a team announcement by sending an email and posting the same update to a Google Chat space.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recipe sends real Gmail and Google Chat messages to configured recipients and spaces.

Mitigation: Review the recipient, Chat space, subject, and announcement text before execution.

Risk: The recipe depends on the gws command and the gws-gmail and gws-chat skills.

Mitigation: Confirm the required tooling and skills are trusted and authorized before installing or running the recipe.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-send-team-announcement)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws command plus trusted gws-gmail and gws-chat skills.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
