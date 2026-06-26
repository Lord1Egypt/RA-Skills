## Description: <br>
Provides weather lookup guidance, practical living and travel suggestions, and seasonal solar-term context for weather-related user questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zcr3344](https://clawhub.ai/user/zcr3344) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer weather, temperature, air quality, umbrella, clothing, and travel-preparation questions with practical advice grounded in queried weather data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may infer a location from conversation history or memory when the user does not provide one. <br>
Mitigation: Ask users to specify a city when they want tighter privacy control, and avoid relying on remembered location hints for external weather lookups. <br>
Risk: Weather data from wttr.in may be incomplete or inaccurate for local decisions. <br>
Mitigation: State uncertainty when results look abnormal and recommend checking the local meteorological authority for official forecasts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zcr3344/xiao-chuang-you-weather) <br>
- [wttr.in Weather Query Endpoint](https://wttr.in/{城市}?format=j1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with weather details and practical recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include current conditions, temperature, feels-like temperature, humidity, wind speed, ultraviolet index, air quality when available, and seasonal solar-term notes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
