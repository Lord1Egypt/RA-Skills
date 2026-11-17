## Description:

Track and analyze cycling performance from Strava, including ride data, fitness trends, workout performance, and automatic new-ride performance analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericrosenberg](https://clawhub.ai/user/ericrosenberg)

### License/Terms of Use:


## Use Case:

External athletes and developers use this skill to connect a Strava account, fetch cycling activities, and receive ride analysis covering power, heart-rate zones, personal records, training load, and fitness trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private Strava activity/profile data and long-lived OAuth tokens.

Mitigation: Use it only when the user is comfortable granting Strava read access; treat the OAuth code, refresh token, client secret, and config file as sensitive credentials.

Risk: The skill stores ride data and logs under the user's home directory.

Mitigation: Restrict ~/.config/strava/config.json to 0600, prefer ~/.cache/strava permissions of 0700 with files set to 0600, and avoid retaining full ride analyses in logs.

Risk: Optional cron monitoring can continue polling Strava and producing analysis after setup.

Mitigation: Review the cron entry before enabling it and remove the entry when automatic monitoring is no longer needed.

## Reference(s):

- [Strava API Reference](references/api.md)
- [Strava API Documentation](https://developers.strava.com/docs/reference/)
- [Strava API Application Settings](https://www.strava.com/settings/api)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown text, JSON activity summaries, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Strava ride metrics, locally cached activity data, and optional Telegram notification text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
