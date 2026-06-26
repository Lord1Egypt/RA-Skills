## Description: <br>
Access global ocean tides model. Functions include tide height at a given date/time/location, tide extrema, and grid weather data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hamandmore](https://clawhub.ai/user/hamandmore) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to query tide heights, tide extrema, and weather-grid variables for specified locations and times through a documented JSON-RPC API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tide and weather lookups send requested coordinates, times, and weather variables to the external API. <br>
Mitigation: Avoid sending sensitive locations or schedules unless that disclosure is acceptable for the intended use. <br>
Risk: Authenticated access uses bearer or opaque basic tokens. <br>
Mitigation: Use a dedicated revocable token and avoid embedding it in shared prompts, logs, or public examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hamandmore/tides) <br>
- [Tides JSON-RPC API endpoint](https://hamandmore.net/api/harmonics/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON, API calls] <br>
**Output Format:** [Markdown guidance with JSON-RPC payloads and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses are returned as JSON-RPC results with structured content when the external API call succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
