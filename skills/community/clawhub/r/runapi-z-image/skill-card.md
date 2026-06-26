## Description: <br>
Generate and edit images with Z-Image through RunAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to route one-off Z-Image generation or editing through the RunAPI CLI and to choose SDKs when integrating Z-Image into an application or backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and related request data may be sent to RunAPI under an API key or saved CLI login. <br>
Mitigation: Use trusted RunAPI credentials, review prompt content before submission, and avoid sending sensitive data unless approved for that service. <br>
Risk: The workflow depends on the external runapi binary and RunAPI service behavior. <br>
Mitigation: Install the CLI from the disclosed source, confirm authentication, and inspect current CLI help or model documentation before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/runapi-ai/runapi-z-image) <br>
- [RunAPI Z-Image Model Overview](https://runapi.ai/models/z-image) <br>
- [RunAPI Z-Image Model Documentation](https://runapi.ai/models/z-image.md) <br>
- [RunAPI Alibaba Provider Comparison](https://runapi.ai/providers/alibaba.md) <br>
- [RunAPI Model Catalog](https://runapi.ai/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and package names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide API-authenticated RunAPI CLI or SDK use for generated image tasks.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
