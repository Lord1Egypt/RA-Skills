## Description: <br>
Get current weather and forecasts using Open-Meteo API (no API key required). Optimized for PowerShell environments with Chinese support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexfeng75](https://clawhub.ai/user/alexfeng75) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
External users and developers use this skill to request current weather and seven-day forecasts through Open-Meteo, especially in PowerShell environments and workflows serving Chinese city lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package advertises PowerShell scripts that are not included in the submitted artifact. <br>
Mitigation: Do not fetch or run similarly named scripts from unverified sources; review any added PowerShell script before execution. <br>
Risk: Weather lookups disclose the selected city coordinates and timezone to Open-Meteo. <br>
Mitigation: Use only location inputs that are appropriate to share with the Open-Meteo service. <br>
Risk: Changing PowerShell execution policy can broaden local script execution permissions. <br>
Mitigation: Avoid execution policy changes unless necessary, and prefer the narrowest user-scoped setting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexfeng75/weather-openmeteo) <br>
- [Open-Meteo documentation](https://open-meteo.com/en/docs) <br>
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with PowerShell command examples and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Weather lookup requests may include city coordinates and timezone values sent to Open-Meteo.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
