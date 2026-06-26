## Description: <br>
Provides YouTube channel statistics, video data, and analytics reporting through youtube-analytics-cli for channel, video, report, and analytics group workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin-huang](https://clawhub.ai/user/bin-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and creators use this skill to fetch YouTube channel or video data, run authenticated analytics reports, and prepare JSON-backed reporting for content performance decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth credentials and refresh tokens can expose private YouTube analytics if mishandled. <br>
Mitigation: Use least-privilege OAuth scopes, keep credentials and refresh tokens out of chat and logs, and restrict permissions on local credential files. <br>
Risk: Analytics commands can access account-specific channel, group, and monetization data. <br>
Mitigation: Use this skill only for YouTube analytics tasks and verify OAuth credentials, scopes, and report parameters before running private reports. <br>


## Reference(s): <br>
- [YouTube Data API v3](https://developers.google.com/youtube/v3) <br>
- [YouTube Analytics API v2](https://developers.google.com/youtube/analytics) <br>
- [YouTube Analytics Reports](https://developers.google.com/youtube/analytics/reference/reports/query) <br>
- [YouTube Analytics Dimensions](https://developers.google.com/youtube/analytics/dimensions) <br>
- [YouTube Analytics Metrics](https://developers.google.com/youtube/analytics/metrics) <br>
- [YouTube Analytics Groups](https://developers.google.com/youtube/analytics/reference/groups/list) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI commands may read YouTube API data and return pretty-printed or compact JSON; errors are JSON on stderr.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
