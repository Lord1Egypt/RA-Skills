## Description: <br>
Stable weather skill for OpenClaw. Designed for reliable same-day weather queries with predictable output, Chinese city support, and automation-friendly plain/json modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paceycrognale](https://clawhub.ai/user/paceycrognale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation builders, and agent operators use this skill to retrieve same-day weather for a single city in predictable plain text, pretty terminal text, or JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: City names or geocoded locations are sent to Open-Meteo over the network. <br>
Mitigation: Use only locations appropriate for disclosure to Open-Meteo and review outbound-network policy before deployment. <br>
Risk: Weather results depend on Open-Meteo availability and returned data. <br>
Mitigation: Handle command failures in automation and verify high-impact weather decisions with an authoritative source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paceycrognale/weather-stable) <br>
- [Open-Meteo](https://open-meteo.com/) <br>
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text, pretty terminal text, or JSON emitted by a Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and outbound access to Open-Meteo; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and release notes) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
