## Description: <br>
Get the weather for a specific location or coordinates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mangonob](https://clawhub.ai/user/mangonob) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to request real-time weather, daily forecasts, or hourly forecasts by location name or longitude and latitude coordinates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses QWeather credentials stored in a configuration file. <br>
Mitigation: Treat privateKey, appId, and credentialId as secrets, keep the config file out of source control, and restrict access to the file. <br>
Risk: Installation relies on an external npm package and network requests. <br>
Mitigation: Before installing, confirm that the npm package and repository are the ones you intend to trust. <br>
Risk: Weather queries can disclose locations or coordinates to the weather provider. <br>
Mitigation: Only submit locations or coordinates you are comfortable sharing with QWeather. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mangonob/skills-weather) <br>
- [QWeather developer documentation](https://dev.qweather.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports location or coordinate input, optional daily or hourly forecast windows, and an optional configuration file path.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
