## Description: <br>
Gets current weather and a short today or tomorrow forecast for the user's configured home location via the Yandex Weather API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alkselsv](https://clawhub.ai/user/alkselsv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and assistants use this skill to answer weather questions for a configured home location, including current conditions and today or tomorrow forecasts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Yandex Weather API key and configured home coordinates, and those coordinates are used when weather requests are handled. <br>
Mitigation: Keep the API key in environment variables, avoid exposing it in responses or files, and use approximate coordinates when exact home location is unnecessary. <br>
Risk: Generic weather phrases may trigger the skill for the configured home location. <br>
Mitigation: Scope activation to weather requests and make clear to users that the default location is the configured home coordinates unless they ask for another location. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alkselsv/yandex-weather-smarthome) <br>
- [Yandex Weather SmartHome onboarding and FAQ](https://yandex.ru/pogoda/b2b/smarthome) <br>
- [Yandex Weather forecast API endpoint](https://api.weather.yandex.ru/v2/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Russian plain text weather template, or JSON when structured output is requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YANDEX_WEATHER_KEY, YANDEX_WEATHER_LAT, and YANDEX_WEATHER_LON; default responses include current temperature, feels-like temperature, condition, wind, and available today or tomorrow forecast fields.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
