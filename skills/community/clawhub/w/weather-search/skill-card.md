## Description: <br>
Query real-time weather information using Amap Weather API for Chinese cities, including weather, temperature, wind, and humidity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[George-China](https://clawhub.ai/user/George-China) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to look up current weather data for Chinese cities by city name, city code, or coordinates through the Amap Weather API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requested city or coordinate weather queries to Amap and requires an Amap API key. <br>
Mitigation: Use only with queries appropriate to send to Amap, keep AMAP_API_KEY scoped where possible, and avoid exposing the key in shared shells, logs, or command histories. <br>


## Reference(s): <br>
- [ClawHub Weather Search Skill Page](https://clawhub.ai/George-China/weather-search) <br>
- [Amap Weather API Documentation](https://lbs.amap.com/api/javascript-api/guide/services/weather) <br>
- [Amap Developer Console](https://console.amap.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and a user-provided AMAP_API_KEY; optional pretty or human-readable formatting uses jq when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
