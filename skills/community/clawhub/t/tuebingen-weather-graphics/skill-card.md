## Description:

Generates a five-day Tübingen weather forecast PNG from Open-Meteo data and prints a short text summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zopyx](https://clawhub.ai/user/zopyx)

### License/Terms of Use:


## Use Case:

Developers and operators can use this skill to generate a visual weather forecast and text summary for Tübingen, including optional scheduling for recurring morning forecast posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional automation can create a recurring daily OpenClaw task that sends weather output through Telegram without enough scoping or removal guidance.

Mitigation: Enable the recurring task only when daily Telegram delivery is intended, keep the script and virtual environment in a private durable location, pin dependencies, and verify how to list and remove the cron entry before deployment.

Risk: The generated forecast depends on live Open-Meteo responses and may be affected by network failures or missing precipitation fields.

Mitigation: Review generated summaries and graphics before sharing when accuracy matters, and add deployment-side handling for API failures or empty precipitation data.

## Reference(s):

- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast?latitude=48.5216&longitude=9.0576)
- [ClawHub Skill Page](https://clawhub.ai/zopyx/skills/tuebingen-weather-graphics)
- [ClawHub Publisher Profile](https://clawhub.ai/user/zopyx)

## Skill Output:

**Output Type(s):** [files, text, shell commands, configuration, guidance]

**Output Format:** [PNG file plus terminal text summary and Markdown instructions with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a forecast image to a local output path and can be scheduled through an OpenClaw cron task.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
