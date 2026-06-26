## Description: <br>
Sends summarized weather alerts for a configured region and supports severity filtering with structured alert counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[li-chi](https://clawhub.ai/user/li-chi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to request summarized weather alert counts for a configured region, optionally filtered by severity. The reviewed implementation is suitable as a placeholder-style alert summary until live weather data retrieval is implemented and verified. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed implementation appears placeholder-style and may not provide real weather alerts until live data retrieval is added. <br>
Mitigation: Treat results as non-authoritative until a trusted weather data source, live retrieval path, and tests for real alert scenarios are implemented and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/li-chi/weather-alert-skill) <br>
- [Release process](docs/release.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [JSON object containing alert_count and summary fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a region input; severity is optional and defaults to all.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence, skill.yaml, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
