## Description: <br>
Get current weather and forecasts (no API key required). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clearlovetop7](https://clawhub.ai/user/clearlovetop7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for simple weather lookup commands, compact forecasts, and JSON weather data without managing API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookups reveal the requested location to the public weather provider. <br>
Mitigation: Avoid submitting sensitive locations, and use only the level of location precision needed for the forecast. <br>
Risk: Weather data and command examples depend on public third-party services. <br>
Mitigation: Prefer HTTPS endpoints where supported and verify results before using them for decisions that require current or exact weather data. <br>
Risk: Publisher identity may matter for installation decisions. <br>
Mitigation: Review the server-resolved publisher profile before installing or relying on the skill. <br>


## Reference(s): <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [Open-Meteo documentation](https://open-meteo.com/en/docs) <br>
- [ClawHub skill page](https://clawhub.ai/clearlovetop7/weatherclear) <br>
- [Publisher profile](https://clawhub.ai/user/clearlovetop7) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and optional JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys required; examples use curl and public weather services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
