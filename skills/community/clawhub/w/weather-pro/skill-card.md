## Description: <br>
Get weather, air quality, sunrise and sunset times, golden and blue hour windows, and sunrise or sunset glow quality forecasts for a requested city. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pazzilivo](https://clawhub.ai/user/Pazzilivo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve concise weather and light-quality planning information for city-based photography and outdoor decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested city or location information is sent to external weather and light-quality services. <br>
Mitigation: Use the skill only for locations you are comfortable sharing with WeatherAPI and Sunsethue. <br>
Risk: The skill loads API keys from ~/.openclaw/.env before calling external services. <br>
Mitigation: Keep that environment file limited to trusted variable assignments and avoid storing unrelated secrets there when using this skill. <br>


## Reference(s): <br>
- [Weather Pro on ClawHub](https://clawhub.ai/Pazzilivo/weather-pro) <br>
- [wttr.in help](https://wttr.in/:help) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text weather summary with command-line usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes weather, air quality, sunrise and sunset times, golden and blue hour windows, and glow quality scores when service responses are available.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
