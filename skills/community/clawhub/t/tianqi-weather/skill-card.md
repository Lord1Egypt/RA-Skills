## Description: <br>
获取天气预报和气温信息。使用场景：用户询问天气、温度、降雨、出行建议等。支持通过 wttr.in 查询全球城市天气，无需 API Key。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmu14641](https://clawhub.ai/user/anmu14641) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query current weather, forecasts, temperature, precipitation, and travel-related weather conditions for global cities through wttr.in. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries a third-party weather service with curl, so responses can be unavailable, rate-limited, or affected by network instability. <br>
Mitigation: Review commands before execution, retry transient failures, and avoid high-frequency repeated requests. <br>
Risk: The skill is not intended for historical weather, severe-weather alerts, or meteorological analysis. <br>
Mitigation: Use official meteorological sources for warnings, emergency decisions, historical records, or analytical weather data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/anmu14641/tianqi-weather) <br>
- [wttr.in Weather Service](https://wttr.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Weather responses depend on wttr.in availability, request limits, network access, and the queried location format.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
