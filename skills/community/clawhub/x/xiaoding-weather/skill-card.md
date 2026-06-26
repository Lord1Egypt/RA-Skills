## Description: <br>
Get current weather and forecasts without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asterisk622](https://clawhub.ai/user/asterisk622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to fetch current weather, compact weather summaries, and forecasts from public weather services via curl. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookups can reveal precise or sensitive locations to public third-party services. <br>
Mitigation: Use coarse locations when possible and avoid querying private addresses or sensitive travel details. <br>
Risk: Some wttr.in examples use a bare host URL that may be interpreted as HTTP by default in shell commands. <br>
Mitigation: Prefer explicit HTTPS URLs, such as https://wttr.in/City, when running weather requests. <br>
Risk: The skill depends on curl and availability of wttr.in or Open-Meteo. <br>
Mitigation: Confirm curl is installed and retry with the fallback Open-Meteo JSON request if the primary service is unavailable. <br>


## Reference(s): <br>
- [ClawHub Weather skill page](https://clawhub.ai/asterisk622/xiaoding-weather) <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [Open-Meteo forecast API documentation](https://open-meteo.com/en/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Files, Guidance] <br>
**Output Format:** [Markdown with inline curl commands, plain-text weather summaries, optional JSON responses, and optional PNG file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; examples contact wttr.in and Open-Meteo public weather services.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
