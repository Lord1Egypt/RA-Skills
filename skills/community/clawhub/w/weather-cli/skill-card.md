## Description: <br>
Gets global city weather forecasts using the free wttr.in API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickcen](https://clawhub.ai/user/nickcen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can request current weather forecasts for global cities, choose Celsius or Fahrenheit, and ask for concise, full, or JSON-formatted output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookups send entered locations to the external wttr.in service. <br>
Mitigation: Use only locations appropriate to share with that service and avoid entering sensitive location data. <br>
Risk: The artifact documents CLI usage but does not bundle the command implementation. <br>
Mitigation: Confirm what provides the weather command before relying on the skill in an agent workflow. <br>
Risk: The documented workflow depends on curl and may require jq for JSON output. <br>
Mitigation: Install dependencies from a trusted package manager and verify they are available before use. <br>


## Reference(s): <br>
- [wttr.in weather service](https://wttr.in) <br>
- [ClawHub skill page](https://clawhub.ai/nickcen/weather-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; command results may be plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a location plus optional unit, full-detail, and JSON flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
