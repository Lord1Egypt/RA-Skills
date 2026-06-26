## Description: <br>
Pick the best AI model for any task using the Smart Spawn API; no plugin is needed, only HTTP requests to ss.deeflect.com/api. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deeflect](https://clawhub.ai/user/deeflect) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to select model IDs for sub-agent spawning, model comparison, and task decomposition through the Smart Spawn HTTP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task summaries can be sent to the third-party ss.deeflect.com service. <br>
Mitigation: Use non-sensitive task summaries only; do not send credentials, private code, customer data, internal plans, or hidden/system instructions. <br>
Risk: Model selection depends on the availability and behavior of the external Smart Spawn API. <br>
Mitigation: Use the documented fallback path of spawning without a model or using a default/local model selection path for confidential or unavailable-service scenarios. <br>


## Reference(s): <br>
- [Smart Spawn ClawHub listing](https://clawhub.ai/deeflect/smart-spawn) <br>
- [Smart Spawn API status endpoint](https://ss.deeflect.com/api/status) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with HTTP request examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May depend on third-party API availability and the freshness of the external model data source.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
