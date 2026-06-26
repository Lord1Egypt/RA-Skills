## Description: <br>
qweather lets agents query QWeather for real-time weather, forecasts, life indices, and city lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deusyu](https://clawhub.ai/user/deusyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to answer weather questions, resolve city names to QWeather location IDs, and fetch current conditions, forecasts, or lifestyle indices through the QWeather API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookups send requested locations to QWeather. <br>
Mitigation: Use the skill only when sharing weather locations with QWeather is acceptable. <br>
Risk: Failed requests may expose the QWeather API key in raw URL error output. <br>
Mitigation: Use a dedicated QWeather API key and avoid sharing raw error output. <br>
Risk: QWEATHER_API_HOST controls the API destination. <br>
Mitigation: Set QWEATHER_API_HOST to the official host assigned in the QWeather console. <br>


## Reference(s): <br>
- [Command Map](references/command-map.md) <br>
- [QWeather Console](https://console.qweather.com) <br>
- [QWeather API Host Settings](https://console.qweather.com/setting) <br>
- [ClawHub Skill Page](https://clawhub.ai/deusyu/rainman-qweather) <br>
- [Publisher Profile](https://clawhub.ai/user/deusyu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language guidance with shell commands and JSON API results when commands are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QWEATHER_API_KEY and QWEATHER_API_HOST; command output depends on QWeather API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
