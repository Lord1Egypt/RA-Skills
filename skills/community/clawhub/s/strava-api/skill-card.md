## Description:

Official Strava OAuth integration for OpenClaw. Use to connect/authorize Strava, store+refresh tokens, and fetch workout/activity data (runs/rides/etc.) for today/yesterday or a date range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swang62](https://clawhub.ai/user/swang62)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to authorize Strava access, refresh stored tokens, and fetch normalized activity data for training summaries, weekly mileage, activity lists, or wellness workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Strava OAuth tokens and private fitness data in local files.

Mitigation: Use a private token path with restrictive permissions, avoid shared export paths, and revoke or rotate Strava credentials if token files are exposed.

## Reference(s):

- [Strava API Quick Reference](references/strava_api.md)
- [Strava Api ClawHub Page](https://clawhub.ai/swang62/skills/strava-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON activity files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Strava OAuth credentials and writes fetched activity data to a user-specified JSON file.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
