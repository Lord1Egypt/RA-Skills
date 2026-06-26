## Description: <br>
Provides current weather conditions and a three-day forecast for a city, coordinate, pinyin input, or IP-based location lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[greenteawater](https://clawhub.ai/user/greenteawater) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer weather requests with current conditions, humidity, wind details, condition icons, and a short forecast. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries are sent to wttr.in, and omitting a location may allow the service to infer location from the request IP. <br>
Mitigation: Provide an explicit city or coordinates when requesting weather and avoid submitting sensitive location details. <br>


## Reference(s): <br>
- [wttr.in weather service](https://wttr.in) <br>
- [ClawHub skill listing](https://clawhub.ai/greenteawater/weather-forecasts222) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown text with inline weather icon image links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes current conditions and up to three daily forecast entries.] <br>

## Skill Version(s): <br>
1.0.5555 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
