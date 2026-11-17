## Description:

Load and analyze Strava activities, stats, and workouts using the Strava API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bohdanpodvirnyi](https://clawhub.ai/user/bohdanpodvirnyi)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent retrieve Strava activities, athlete profile data, workout details, and aggregate stats for fitness analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Strava account data may include private workouts, routes, timestamps, and heart-rate metrics.

Mitigation: Grant only the Strava scopes needed for the task and keep access tokens in a protected secret store or restricted-permission configuration file.

Risk: The token refresh helper can expose full account access credentials in normal command output.

Mitigation: Avoid running the refresh helper in logged terminals or shared agent sessions unless it is fixed to avoid printing full tokens.

## Reference(s):

- [Strava Developers](https://developers.strava.com/)
- [Strava API Reference](https://developers.strava.com/docs/reference/)
- [Create a Strava API Application](https://www.strava.com/settings/api)
- [ClawHub Strava Skill](https://clawhub.ai/bohdanpodvirnyi/skills/strava)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with inline shell commands, curl examples, configuration snippets, and summarized Strava API results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and Strava OAuth credentials, including STRAVA_ACCESS_TOKEN for read access.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
