## Description:

Launches a personalized AI wellness coach video session using Tavus CVI and Claude, with wearable health data, Google Calendar context, wellness recommendations, and optional Telegram morning briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrechuabio](https://clawhub.ai/user/andrechuabio)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to start a personalized wellness coaching session or daily morning briefing that combines health metrics, calendar context, and video-based coaching guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive wearable health metrics and calendar details across multiple services.

Mitigation: Use only trusted service accounts and recipients, limit shared data to the minimum needed, and review provider permissions before enabling integrations.

Risk: The setup asks users to run unpinned external code and store API tokens for Tavus, Anthropic, Google Calendar, wearable providers, and optional Telegram delivery.

Mitigation: Install a pinned and verified repository version in an isolated environment, keep secrets outside the project directory when possible, and rotate tokens if exposure is suspected.

Risk: The daily cron and HEARTBEAT forwarding flow can repeatedly send health and calendar summaries externally.

Mitigation: Enable recurring automation only after confirming the destination, schedule, disable path, and acceptable disclosure level.

## Reference(s):

- [Wellness Coach AI ClawHub Page](https://clawhub.ai/andrechuabio/skills/wellness-coach)
- [Google Calendar Setup](references/gcal-setup.md)
- [OpenClaw Cron Setup](references/openclaw-cron.md)
- [Wearable Integration Guide](references/wearables.md)
- [Oura API Daily Sleep Endpoint](https://api.ouraring.com/v2/usercollection/daily_sleep)
- [Fitbit Sleep API Endpoint](https://api.fitbit.com/1.2/user/-/sleep/date/today.json)
- [Terra API](https://tryterra.co)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, API endpoint descriptions, and wellness recommendation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create external Tavus session links and Telegram briefing messages when configured by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
