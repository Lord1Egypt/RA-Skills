## Description: <br>
查询全球城市或者经纬度位置的实时天气、天气预报、空气质量等信息的技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinguobing](https://clawhub.ai/user/yinguobing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for current weather, forecasts, air quality, weather warnings, and location-based QWeather data for cities or coordinates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a QWeather private key and related project credentials. <br>
Mitigation: Keep the private key file permission-restricted and do not share credentials in logs, prompts, or generated output. <br>
Risk: Installation depends on the published Cargo package or the linked GitHub source. <br>
Mitigation: Install only when the package or source repository is trusted for the deployment environment. <br>
Risk: Custom QWEATHER_BASE_URL and QWEATHER_GEO_URL values control where weather requests are sent. <br>
Mitigation: Verify both base URLs point to the intended QWeather endpoints before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinguobing/qweather-skill) <br>
- [QWeather skill homepage](https://github.com/yinguobing/qweather-skill) <br>
- [QWeather project console](https://console.qweather.com/project) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown weather guidance with inline shell commands when setup or CLI usage is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QWeather credentials and configured QWeather API base URLs; supported forecast ranges vary by command.] <br>

## Skill Version(s): <br>
0.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
