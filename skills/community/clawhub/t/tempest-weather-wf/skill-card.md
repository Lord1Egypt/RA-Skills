## Description: <br>
Fetches live weather data from a WeatherFlow Tempest weather station and returns structured JSON with current conditions, wind, precipitation, and lightning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mogglemoss](https://clawhub.ai/user/mogglemoss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent fetch and normalize live observations from their WeatherFlow Tempest station, including current conditions, wind, rain, lightning, solar readings, and station status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a WeatherFlow Tempest token and station ID, which could expose account or station access if pasted into chat, committed to files, or shared. <br>
Mitigation: Keep credentials in environment or secret storage, avoid pasting tokens into prompts or dotfiles, and rotate or revoke the token if it is exposed. <br>
Risk: Station responses may include precise latitude, longitude, timezone, elevation, or other location-linked weather data. <br>
Mitigation: Review returned JSON before sharing it and remove location fields when the recipient does not need them. <br>


## Reference(s): <br>
- [WeatherFlow Tempest REST API](https://weatherflow.github.io/Tempest/api/) <br>
- [Tempest Weather System](https://weatherflow.com/tempest-weather-system/) <br>
- [Tempest Observation Field Reference](references/obs_fields.md) <br>
- [ClawHub skill page](https://clawhub.ai/mogglemoss/tempest-weather-wf) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Configuration guidance] <br>
**Output Format:** [Structured JSON with optional Markdown guidance for setup or API errors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TEMPEST_TOKEN and TEMPEST_STATION_ID to fetch current station observations; responses may include station location fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
