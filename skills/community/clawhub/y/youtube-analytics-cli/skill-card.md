## Description:

Provides YouTube channel statistics, video details, and analytics reporting through youtube-analytics-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin-huang](https://clawhub.ai/user/bin-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and YouTube channel operators use this skill to fetch channel and video data, run analytics reports with dimensions and filters, and inspect analytics groups through a CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run an unpinned third-party CLI that handles OAuth refresh tokens and private YouTube analytics data.

Mitigation: Use a pinned, verified CLI version in an isolated environment before granting access to YouTube account data.

Risk: OAuth credentials, refresh tokens, client secrets, and credential files could expose private analytics data if shared in chat or logs.

Mitigation: Never paste secrets or credential file contents into chat or logs, and grant only the minimum YouTube OAuth scopes needed.

Risk: The monetary-read scope can expose revenue-related analytics.

Mitigation: Avoid the monetary-read scope unless revenue reporting is required for the task.

## Reference(s):

- [YouTube Analytics CLI documentation](https://github.com/Bin-Huang/youtube-analytics-cli)
- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [YouTube Analytics API v2](https://developers.google.com/youtube/analytics)
- [YouTube Analytics reports query reference](https://developers.google.com/youtube/analytics/reference/reports/query)
- [YouTube Analytics dimensions](https://developers.google.com/youtube/analytics/dimensions)
- [YouTube Analytics metrics](https://developers.google.com/youtube/analytics/metrics)
- [ClawHub skill page](https://clawhub.ai/bin-huang/skills/youtube-analytics-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI commands return pretty-printed JSON by default or compact JSON when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
