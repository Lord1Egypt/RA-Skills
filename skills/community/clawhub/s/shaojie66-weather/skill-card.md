## Description: <br>
Get current weather and forecasts via wttr.in or Open-Meteo for location-based weather, temperature, and forecast questions without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaojie66](https://clawhub.ai/user/shaojie66) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to answer current weather, temperature, rain, and short forecast questions for a city, region, or airport code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather requests contact wttr.in and can reveal the queried location plus normal request metadata such as IP address. <br>
Mitigation: Use city, region, or airport codes instead of exact home addresses or sensitive travel details. <br>
Risk: The Open-Meteo capability is mentioned in the skill description but not documented in the provided commands. <br>
Mitigation: Expect wttr.in behavior unless the publisher updates the skill with explicit Open-Meteo usage. <br>


## Reference(s): <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [ClawHub skill page](https://clawhub.ai/shaojie66/shaojie66-weather) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, images] <br>
**Output Format:** [Markdown guidance with curl commands that return text summaries, detailed forecasts, JSON, or PNG weather output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and sends weather queries to wttr.in; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
