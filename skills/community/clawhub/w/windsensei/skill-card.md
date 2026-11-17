## Description:

Check wind and weather conditions for wind sports (kitesurfing, wingfoiling, surfing). Get forecasts, find spots nearby, view session history, and request new spots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jumptrnr](https://clawhub.ai/user/jumptrnr)

### License/Terms of Use:


## Use Case:

External users use this skill to check wind-sport forecasts, compare nearby or saved spots, review session history, and request new spot additions through WindSensei data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated use can expose saved spots, session history, and followed-user live activity.

Mitigation: Install only when that WindSensei account access is acceptable, and review live-session responses for privacy before sharing them.

Risk: The API key can be passed in less private ways such as query parameters.

Mitigation: Prefer Bearer-token authentication and avoid putting API keys in URLs.

Risk: Calendar actions may create multiple events from forecast blocks.

Mitigation: Confirm calendar events before allowing bulk creation.

Risk: Remote response hints and forecast summaries could influence user-facing guidance.

Mitigation: Report only what the API data says and do not invent or upgrade condition quality.

## Reference(s):

- [WindSensei](https://windsensei.com)
- [WindSensei API key profile page](https://windsensei.com/dashboard/profile)
- [ClawHub skill page](https://clawhub.ai/jumptrnr/skills/windsensei)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown and concise text summaries with API request guidance and optional calendar event details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an optional WINDSENSEI_API_KEY for personalized forecasts, saved spots, session history, and live followed-user activity.]

## Skill Version(s):

1.4.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
