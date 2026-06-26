## Description: <br>
Get current weather and forecasts without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent produce quick weather lookup commands, compact current-condition requests, full forecasts, and JSON weather API examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookups may disclose requested locations to public weather providers. <br>
Mitigation: Use only locations appropriate to share with those providers and avoid sensitive precise-location queries. <br>
Risk: Example commands may be copied with provider URLs that are not explicitly HTTPS. <br>
Mitigation: Prefer explicit HTTPS URLs when adapting curl commands for real use. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/litiao1224/weather-litiao) <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [Open-Meteo documentation](https://open-meteo.com/en/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with bash code blocks and weather API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; weather requests may send requested locations to public weather providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
