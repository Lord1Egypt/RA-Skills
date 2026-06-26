## Description: <br>
Get current weather and forecasts via open-meteo.com with optional fallback to wttr.in if available. No API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vdiogov](https://clawhub.ai/user/vdiogov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to answer weather, forecast, temperature, or rain-probability questions for a location using public weather APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookups may send exact private coordinates or sensitive locations to Open-Meteo or wttr.in. <br>
Mitigation: Avoid exact private coordinates or sensitive locations when privacy is a concern. <br>
Risk: Fallback requests to wttr.in may use non-HTTPS endpoints in the artifact examples. <br>
Mitigation: Prefer HTTPS endpoints where available. <br>


## Reference(s): <br>
- [Open-Meteo](https://open-meteo.com/) <br>
- [Open-Meteo API docs](https://open-meteo.com/en/docs) <br>
- [ClawHub skill page](https://clawhub.ai/vdiogov/weather-open-meteo) <br>
- [Publisher profile](https://clawhub.ai/user/vdiogov) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with inline shell commands and weather summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; queries Open-Meteo and may fall back to wttr.in.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
