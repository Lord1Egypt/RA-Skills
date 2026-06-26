## Description: <br>
Get current weather and forecasts with no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happyzengfen](https://clawhub.ai/user/happyzengfen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current weather, compact forecasts, full text forecasts, and fallback JSON weather data from public weather services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather requests can disclose exact private addresses or sensitive locations to public weather services. <br>
Mitigation: Use broader city, airport, or regional identifiers when location privacy matters. <br>
Risk: The primary examples use wttr.in URLs without an explicit HTTPS scheme. <br>
Mitigation: Prefer HTTPS endpoints when running curl requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/happyzengfen/weather-test-1774063891) <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true) <br>
- [Open-Meteo documentation](https://open-meteo.com/en/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples, text weather responses, PNG output guidance, and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the documented command examples; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
