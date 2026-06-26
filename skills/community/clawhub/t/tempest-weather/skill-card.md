## Description: <br>
Get current weather conditions from a WeatherFlow Tempest station using the Tempest REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wranglerdriver](https://clawhub.ai/user/wranglerdriver) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to retrieve current backyard or home weather readings and historical day, month, or year statistics from their WeatherFlow Tempest station. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Tempest API token to read station data. <br>
Mitigation: Store the token in environment configuration and avoid sharing it in chat or skill files. <br>
Risk: Broad home or backyard weather requests may expose station-specific data rather than general public weather. <br>
Mitigation: Use the skill only where station-level weather data is appropriate for the requester and environment. <br>


## Reference(s): <br>
- [Tempest API Notes](references/tempest-api.md) <br>
- [Project homepage](https://github.com/wranglerdriver/tempest-weather) <br>
- [Tempest platform](https://tempest.earth) <br>
- [ClawHub skill page](https://clawhub.ai/wranglerdriver/tempest-weather) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [JSON with an optional concise human-readable weather summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TEMPEST_API_TOKEN and a station or device ID; supports US or metric units and day, month, or year statistics.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
