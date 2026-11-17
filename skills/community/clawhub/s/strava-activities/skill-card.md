## Description:

Track and manage Strava workouts, athlete stats, routes, segments, and club activities via the Strava API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect a Strava account through ClawLink, inspect activities and athlete data, explore routes and segments, and perform account-authorized Strava actions from an agent chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and allowlist an unpinned third-party plugin that can persist across chats and mediate sensitive Strava account access.

Mitigation: Install only if the user trusts ClawLink and the ClawHub plugin source; revoke the Strava connection and remove the plugin when it is no longer needed.

Risk: Write operations can change or delete activities, routes, equipment, comments, kudos, and club membership.

Mitigation: Prefer read-only OAuth scopes where possible, describe and preview write actions, and execute them only after explicit user confirmation.

Risk: Strava activity data may include sensitive fitness, location, route, and privacy-controlled account information.

Mitigation: Limit OAuth scopes to the user's intended task and avoid exposing private activity details unless the user has requested that access.

## Reference(s):

- [Strava API Documentation](https://developers.strava.com/docs/reference/)
- [Strava API Overview](https://developers.strava.com/)
- [Strava Authentication](https://developers.strava.com/docs/auth/)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=strava-activities)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses authenticated ClawLink Strava tools and should preview or confirm write actions before execution.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
