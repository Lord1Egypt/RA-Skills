## Description:

Smart Surprise proactively sends personalized casual messages at randomized intervals, learns user preferences, and schedules future check-ins through a self-renewing cron workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turingcorp-net](https://clawhub.ai/user/turingcorp-net)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use Smart Surprise when they want an agent to initiate occasional personalized check-ins, practical tips, news, weather-aware suggestions, or lightweight conversation through a configured messaging channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates an indefinite self-renewing cron chain that can continue sending surprise messages.

Mitigation: Enable it only intentionally, configure quiet hours and interval bounds before activation, and keep the documented stop procedure for removing Smart Surprise cron jobs available.

Risk: The skill stores learned user preferences in topics.md and updates them over time.

Mitigation: Review topics.md before enabling the skill and periodically audit or edit learned preferences to correct unwanted personalization.

Risk: The optional calendar topic may read sensitive Google Calendar OAuth credentials.

Mitigation: Leave calendar disabled unless a trusted credential setup is in place, and provide only the minimum credential access needed for calendar reminders.

## Reference(s):

- [Smart Surprise Skill Page](https://clawhub.ai/turingcorp-net/skills/smart-surprise)
- [Smart Surprise Setup Procedure](references/setup.md)
- [Smart Surprise Configuration Reference](references/config.md)
- [Smart Surprise Topics Reference](references/topics.md)
- [wttr.in Weather JSON Endpoint](https://wttr.in/{location}?format=j1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples; runtime output is plain user-facing message text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime messages are personalized from config and topics state; no fixed token cap is specified.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
