## Description: <br>
Get current weather and forecasts (no API key required). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quincygunter](https://clawhub.ai/user/quincygunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve current conditions and forecasts for a location through no-key weather services, with wttr.in as the primary endpoint and Open-Meteo JSON as a fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to run curl commands against external weather services, so users could expose location queries or rely on stale or unavailable third-party responses. <br>
Mitigation: Review the generated command before execution, avoid including sensitive location details when unnecessary, and validate important forecasts against an authoritative source. <br>


## Reference(s): <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [Open-Meteo forecast API documentation](https://open-meteo.com/en/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash examples, plain-text weather summaries, and optional JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; weather data depends on the availability and accuracy of external weather services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
