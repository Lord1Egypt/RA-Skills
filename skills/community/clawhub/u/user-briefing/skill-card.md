## Description:

Provides a personalized morning briefing with current weather, upcoming calendar events, important emails, and top pending tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sai-sh](https://clawhub.ai/user/sai-sh)

### License/Terms of Use:


## Use Case:

Individuals and agent users use this skill to assemble a morning briefing from weather, Google Calendar, Gmail, and Google Tasks data before planning their day.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment says the skill asks for sensitive Google and Gmail tokens in a plaintext .env file.

Mitigation: Use least-privilege, revocable, short-lived tokens; avoid storing long-lived account tokens in plaintext; rotate credentials after testing.

Risk: The security assessment says the skill includes mutable remote verification text in its output.

Mitigation: Remove or disable the remote verification behavior before routine use and treat any returned verification text as untrusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sai-sh/skills/user-briefing)
- [OpenWeather API](https://openweathermap.org/api)
- [Google Calendar API](https://developers.google.com/calendar/api/quickstart)
- [Gmail API](https://developers.google.com/gmail/api/reference/rest)
- [Google Tasks API](https://developers.google.com/tasks/reference/rest)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text briefing with section headings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes partial results or service-specific error messages when configured APIs are unavailable.]

## Skill Version(s):

1.0.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
