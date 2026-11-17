## Description:

Review who attended a Google Meet conference and for how long.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workspace administrators use this recipe to review recent Google Meet conference attendance, participant lists, and session durations using an authenticated Google Workspace CLI account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting attendance data may reveal private participant identities and timing information.

Mitigation: Use the skill only with accounts authorized to query the relevant Google Meet conference records, and review attendance details before sharing them outside the intended audience.

Risk: The recipe depends on the configured gws account and may expose any conference records that account can access.

Mitigation: Configure gws with least-privilege Google Workspace access appropriate for the review task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/recipe-review-meet-participants)
- [ClawHub publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only Google Meet attendance review steps for an authenticated gws account.]

## Skill Version(s):

1.0.12 (source: server release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
