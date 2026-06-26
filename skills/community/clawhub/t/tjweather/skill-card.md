## Description: <br>
全球地点天气预报及地理编码分析（TJWeather API）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiansonguio](https://clawhub.ai/user/qiansonguio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to geocode a requested place, query TJWeather forecasts, and return concise weather statistics with a short practical summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location queries may be sent to TJWeather and, for geocoding, to OpenStreetMap Nominatim or Photon. <br>
Mitigation: Avoid entering sensitive exact addresses unless that precision is needed. <br>
Risk: API keys may be exposed if configured as plain text. <br>
Mitigation: Use a personal TJWeather API key and prefer SecretRef or environment-variable configuration. <br>
Risk: Forecast requests beyond the documented 10-day limit may not be fully supported. <br>
Mitigation: Limit forecast requests to 10 days or clearly tell the user that only the first 10 days are shown. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qiansonguio/tjweather) <br>
- [TJWeather API Homepage](https://api.tjweather.com) <br>
- [TJWeather Website](https://www.tjweather.com/) <br>
- [TJWeather API Key Application](https://www.tjweather.com/Apply) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with weather statistics, command-driven tool use, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and TJWEATHER_API_KEY; forecast output is documented for up to 10 days.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
