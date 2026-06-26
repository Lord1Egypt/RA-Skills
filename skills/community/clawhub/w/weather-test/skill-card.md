## Description: <br>
Get current weather and forecasts without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erhwenkuo](https://clawhub.ai/user/erhwenkuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current weather and forecasts with curl from wttr.in or Open-Meteo when no weather API key is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries are sent to public weather providers and can reveal locations of interest. <br>
Mitigation: Use non-sensitive or approximate locations and avoid querying locations that should not be shared with public providers. <br>
Risk: The documented commands depend on public weather services whose availability and responses are outside the skill publisher's control. <br>
Mitigation: Review returned weather data before acting on it and use Open-Meteo as a fallback when wttr.in is unavailable. <br>


## Reference(s): <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [Open-Meteo documentation](https://open-meteo.com/en/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, JSON] <br>
**Output Format:** [Markdown guidance with inline bash commands and example JSON API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the documented wttr.in commands; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
