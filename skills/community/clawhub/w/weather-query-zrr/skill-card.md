## Description: <br>
Queries current weather, 3-day forecasts, and air quality for global cities using wttr.in and Open-Meteo without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zrr000212-netizen](https://clawhub.ai/user/zrr000212-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to answer city-level weather, forecast, and air-quality requests from an agent by running a local Python command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script sends the provided city or location name to public weather APIs. <br>
Mitigation: Use only locations the user intends to share and avoid entering private addresses or sensitive location context. <br>
Risk: Weather and air-quality results depend on third-party service availability and response quality. <br>
Mitigation: Prefer the alternate Open-Meteo source when wttr.in is unavailable, and treat returned weather data as informational. <br>
Risk: The skill runs a local Python script that makes outbound HTTPS requests. <br>
Mitigation: Review the script and network behavior before installation in restricted environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zrr000212-netizen/weather-query-zrr) <br>
- [wttr.in](https://wttr.in/) <br>
- [Open-Meteo API documentation](https://open-meteo.com/en/docs) <br>
- [wttr.in internationalization](https://github.com/chubin/wttr.in#internationalization) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON from a Python CLI, with Markdown command examples in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports current weather, 3-day forecast, and air-quality modes; accepts city, source, language, and output-format options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
