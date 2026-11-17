## Description:

Send daily 08:00 weather reports for Tübingen using open-meteo.com. Use when Master wants an automated summary (current conditions + today’s high/low + rain chance) stored locally and forwarded via Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zopyx](https://clawhub.ai/user/zopyx)

### License/Terms of Use:


## Use Case:

Users and automation operators use this skill to fetch, save, and forward a concise daily weather summary for Tübingen, including current conditions, temperature range, and rain probability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional cron setup creates a recurring task that continues making daily network requests, writing reports, and forwarding summaries until it is removed.

Mitigation: Enable the cron example only when recurring reports are desired, and remove the cron entry when automatic daily delivery is no longer needed.

## Reference(s):

- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast?latitude=48.5216&longitude=9.0576)
- [ClawHub Skill Page](https://clawhub.ai/zopyx/skills/tuebingen-weather)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text weather summary with optional saved text file and cron configuration snippet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write reports under data/weather and may forward summaries automatically when the cron example is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
