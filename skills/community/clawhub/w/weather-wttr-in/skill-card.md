## Description: <br>
Get weather data from wttr.in free service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[etmnb](https://clawhub.ai/user/etmnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve current weather and short-term forecasts for cities, coordinates, or an IP-inferred location without configuring an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries are sent to wttr.in, and no-location mode can let the service infer an approximate location from the user's IP address. <br>
Mitigation: Use an explicit city name or coordinate when possible and install the skill only if sending weather queries to wttr.in is acceptable. <br>


## Reference(s): <br>
- [wttr.in weather service](https://wttr.in) <br>
- [ClawHub skill page](https://clawhub.ai/etmnb/weather-wttr-in) <br>
- [Publisher profile](https://clawhub.ai/user/etmnb) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Console text or formatted JSON from a Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns current conditions and a three-day forecast; optional flags select JSON output, daily summary, language, and explicit location.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
