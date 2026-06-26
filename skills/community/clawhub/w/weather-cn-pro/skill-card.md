## Description: <br>
Weather CN Pro queries Chinese city weather from China Weather Network and returns current conditions, lifestyle indexes, hourly forecasts, and seven-day forecasts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziqi-jin](https://clawhub.ai/user/ziqi-jin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a shell-based Chinese weather lookup for supported city names and receive formatted weather, lifestyle index, hourly forecast, and seven-day forecast output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The shell script evaluates parsed remote weather text as shell code. <br>
Mitigation: Review before installation and replace eval-based parsing with explicit variable assignment or structured parsing before deployment. <br>
Risk: The artifact contains an under-disclosed third-party AQI helper endpoint. <br>
Mitigation: Document the AQI network destination and data behavior, or remove the helper if it is not needed. <br>
Risk: The skill makes outbound network requests from a bash script. <br>
Mitigation: Use only in environments where outbound requests to the weather data sources are acceptable and network behavior has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ziqi-jin/weather-cn-pro) <br>
- [China Weather Network data source](https://www.weather.com.cn/) <br>
- [AQI helper endpoint host](https://api.aooi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text output from a bash script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and grep; city lookup depends on bundled weather_codes.txt entries or built-in city mappings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and script header) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
