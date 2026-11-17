## Description:

Generate daily Weather Intelligence Digest using NOAA/NWS data with customizable locations and alert monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannyboy1241](https://clawhub.ai/user/dannyboy1241)

### License/Terms of Use:


## Use Case:

External users, developers, and operations teams use this skill to generate location-based weather briefings with forecasts and active alert summaries for publication, email, dashboards, or automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured latitude and longitude values are sent to NOAA/NWS when forecasts and alerts are requested.

Mitigation: Use only locations you are comfortable sharing with NOAA/NWS and avoid sensitive private coordinates.

Risk: Optional Slack, heartbeat, cron, LaunchAgent, Things, and Reminders recipes can distribute weather output or run on a schedule.

Mitigation: Enable automation only with user intent, review recipients and channels, and document how to disable scheduled jobs.

Risk: Generated HTML may include dynamic weather fields from external data sources.

Mitigation: Review or escape dynamic fields before publishing or embedding generated HTML.

Risk: Unpinned Python dependency ranges can reduce install reproducibility over time.

Mitigation: Use pinned dependencies or a lockfile for controlled deployments.

## Reference(s):

- [Weather Digest on ClawHub](https://clawhub.ai/dannyboy1241/skills/weather-digest)
- [NOAA/NWS API](https://api.weather.gov)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML, and JSON files with CLI setup and automation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, pip, requests, and a JSON configuration containing location names with latitude and longitude.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
