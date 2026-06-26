## Description: <br>
Provides a personalized morning briefing with current weather, upcoming calendar events, important emails, and top pending tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sai-sh](https://clawhub.ai/user/sai-sh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals and agents use this skill to assemble a morning briefing from OpenWeather and read-only Google Calendar, Gmail, and Tasks data. It is useful for preparing a concise day-at-a-glance summary before work starts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private Google Calendar, Gmail, and Tasks data and reads API credentials from a local .env file. <br>
Mitigation: Use least-privilege read-only Google tokens, keep the .env file private, and rotate or remove credentials when they are no longer needed. <br>
Risk: The security evidence flags an under-explained remote verification step before the briefing is produced. <br>
Mitigation: Review the verification behavior before installation and prefer removing or disabling the remote verification step before routine use. <br>
Risk: Missing, expired, or over-broad API tokens can produce incomplete results or expose more account data than needed. <br>
Mitigation: Provide only the specific tokens required for enabled briefing sections, use short-lived credentials where possible, and disable unused sections in config.json. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sai-sh/user-briefing) <br>
- [Publisher Profile](https://clawhub.ai/user/sai-sh) <br>
- [OpenWeather API](https://openweathermap.org/api) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>
- [Google Calendar API Quickstart](https://developers.google.com/calendar/api/quickstart) <br>
- [Gmail API Reference](https://developers.google.com/gmail/api/reference/rest) <br>
- [Google Tasks API Reference](https://developers.google.com/tasks/reference/rest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text briefing with setup commands and optional JSON and .env configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches fresh data on each run; weather, calendar, email, and task sections can be controlled through config.json.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
