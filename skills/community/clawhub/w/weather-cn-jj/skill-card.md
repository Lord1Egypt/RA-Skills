## Description: <br>
国内天气+空气质量查询。支持城市和区县级，中文输出。数据源: wttr.in + Open-Meteo。无需 API Key。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lujun2508](https://clawhub.ai/user/lujun2508) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Chinese city or district weather, optional air-quality data, tomorrow forecasts, and clothing guidance in Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookups send the searched city or district to wttr.in, and AQI lookups send coordinates to Open-Meteo. <br>
Mitigation: Avoid querying sensitive personal locations when location privacy matters. <br>
Risk: Weather and AQI results depend on third-party data sources and may be delayed or unavailable. <br>
Mitigation: Treat results as informational and verify important decisions against authoritative local forecasts or air-quality sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lujun2508/weather-cn-jj) <br>
- [Publisher profile](https://clawhub.ai/user/lujun2508) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Plain text and Markdown with inline bash and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Chinese weather, AQI, forecast, and clothing-advice responses; requires Python and external requests to wttr.in and Open-Meteo.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
