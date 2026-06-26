## Description: <br>
Get current weather and forecasts through wttr.in without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[164149043](https://clawhub.ai/user/164149043) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to compose curl-based weather lookups for current conditions, forecasts, compact weather formats, and location-specific weather queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather queries, including specific locations or coordinates, leave the user's machine when the generated curl commands are run. <br>
Mitigation: Avoid exact home addresses, internal site names, or sensitive coordinates unless they are intended to be shared with the public weather provider. <br>


## Reference(s): <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [ClawHub skill page](https://clawhub.ai/164149043/weather-tools) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; location and format selections are sent to wttr.in when commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
