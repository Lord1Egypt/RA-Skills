## Description: <br>
Gets current weather conditions and forecasts for user-specified locations through WeatherAPI.com after the user configures a WeatherAPI API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianmo1997](https://clawhub.ai/user/jianmo1997) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to answer weather, temperature, rain, and forecast questions for global locations with the user's own WeatherAPI.com credential. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather locations are sent to WeatherAPI.com when the skill runs. <br>
Mitigation: Use only locations the user is comfortable sharing with WeatherAPI.com, and avoid unnecessarily precise or sensitive location queries. <br>
Risk: A locally stored WeatherAPI key could be exposed through copied configuration, logs, or troubleshooting output. <br>
Mitigation: Store the key locally, avoid sharing configuration or log excerpts that include it, and redact the key before posting diagnostics. <br>
Risk: Adapted location queries may break or be misinterpreted if unsafe characters are passed directly into request URLs. <br>
Mitigation: URL-encode user-provided location strings before constructing WeatherAPI.com request URLs. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/jianmo1997/shulian-weather) <br>
- [WeatherAPI.com](https://www.weatherapi.com/) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jianmo1997) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API response expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and a user-provided WEATHER_API_KEY; WeatherAPI.com receives the queried location and returns JSON weather data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
