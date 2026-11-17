## Description:

Queries China-focused sunset, sunrise, and colorful-cloud forecasts from sunsetbot.top and guides agents through threshold-based notification and logging workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neverland83](https://clawhub.ai/user/neverland83)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to check China domestic sunrise and sunset forecast conditions, decide whether the forecast crosses a notification threshold, optionally send a Feishu alert, and keep local JSONL and Markdown monitoring logs.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can use a Feishu Open ID to send notifications.

Mitigation: Keep the Open ID in config/config.json and review the notification target before enabling alerts.

Risk: Cron setup can run recurring forecast checks and append local weather logs.

Mitigation: Review the cron schedule, timezone, payload, and log location before enabling recurring monitoring.

Risk: Forecast quality depends on the external sunsetbot.top service response.

Mitigation: Treat results as forecast guidance and inspect returned fields before acting on unusual or high-impact alerts.

## Reference(s):

- [SunsetBot forecast service](https://sunsetbot.top/)
- [ClawHub skill page](https://clawhub.ai/neverland83/skills/sunsetbot-monitor-cn)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, JSONL, API-call, notification, and cron configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append local JSONL and Markdown logs and optionally send a Feishu notification when the forecast threshold is met.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
