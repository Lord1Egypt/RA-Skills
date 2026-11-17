## Description:

Gets current weather and a short today/tomorrow forecast for the user's configured home location via the Yandex Weather API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alkselsv](https://clawhub.ai/user/alkselsv)

### License/Terms of Use:

MIT-0

## Use Case:

External users and home-automation agents use this skill to answer current weather and short forecast requests for a configured home location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Yandex Weather API key and configured home coordinates.

Mitigation: Store the API key only in environment variables and deploy only where sending the configured coordinates to Yandex is acceptable.

Risk: Default responses are localized to Russian.

Mitigation: Set user expectations for Russian weather output or request structured JSON when downstream handling needs a language-neutral format.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alkselsv/skills/yandex-weather-smarthome)
- [Yandex Weather SmartHome onboarding](https://yandex.ru/pogoda/b2b/smarthome)
- [Yandex Weather Forecast API endpoint](https://api.weather.yandex.ru/v2/forecast)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text weather summary with fixed labels; optional JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YANDEX_WEATHER_KEY, YANDEX_WEATHER_LAT, and YANDEX_WEATHER_LON; default user-facing output is Russian.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
