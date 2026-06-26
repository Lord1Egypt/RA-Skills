## Description: <br>
Get current weather and forecasts without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tongguanghai](https://clawhub.ai/user/tongguanghai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to look up current weather and forecasts with public weather services through curl commands and JSON weather API examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries are sent to public third-party services. <br>
Mitigation: Use the skill only when sharing the queried location with wttr.in or Open-Meteo is acceptable. <br>
Risk: Server evidence reports unavailable provenance and notes that embedded artifact metadata differs from the registry listing. <br>
Mitigation: Rely on the server-resolved publisher handle and listing URL when evaluating publisher identity. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/tongguanghai/weather-test1) <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [Open-Meteo forecast API example](https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true) <br>
- [Open-Meteo documentation](https://open-meteo.com/en/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
