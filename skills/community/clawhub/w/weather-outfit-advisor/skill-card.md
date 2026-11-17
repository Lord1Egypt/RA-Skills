## Description:

Query weather and provide outfit recommendations. When information is insufficient, ask about destination, date, and clothing preferences. Uses free weather APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kadijin](https://clawhub.ai/user/kadijin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn destination, travel date, and clothing preferences into weather-aware outfit guidance. It can also call helper scripts for forecast JSON and optional outfit reference image search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destination, travel date, clothing preferences, and image-search terms may be sent to external weather and image services.

Mitigation: Tell users about these data flows before use and avoid sending sensitive personal details in prompts or script arguments.

Risk: The artifact includes a hardcoded Pexels API key.

Mitigation: Replace embedded credentials with user-provided secure configuration and rotate the exposed key before deployment.

Risk: Weather forecasts, image search results, or service availability may be incomplete or inaccurate.

Mitigation: Review outputs before relying on them, verify severe-weather conditions with local sources, and provide manual weather details when API calls fail.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kadijin/skills/weather-outfit-advisor)
- [wttr.in weather API](https://wttr.in/{city}?format=j1)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Pexels API](https://www.pexels.com/api/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown outfit advice with optional JSON weather and image-search outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include destination, date, weather summary, outfit recommendations, cautions, backup plans, and image reference links.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
