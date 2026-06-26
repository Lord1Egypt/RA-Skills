## Description: <br>
Generate and edit images with Nano Banana through RunAPI, using the CLI for one-off tasks and SDKs for application integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to create, edit, or transform images with Nano Banana through RunAPI. Developers use it to decide when to call the RunAPI CLI for one-off tasks and when to use SDKs for application integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a RunAPI API key or saved CLI authentication to submit image requests to a third-party service. <br>
Mitigation: Use a dedicated API key where possible, install the RunAPI CLI only from trusted sources, and avoid sending secrets, private documents, or sensitive images unless that use is approved. <br>
Risk: Generated or edited images may reflect prompt mistakes, policy constraints, or model limitations. <br>
Mitigation: Review generated images before use and keep request files free of sensitive content unless the workflow has been approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runapi-ai/runapi-nano-banana) <br>
- [RunAPI Nano Banana model overview](https://runapi.ai/models/nano-banana) <br>
- [RunAPI Nano Banana model documentation](https://runapi.ai/models/nano-banana.md) <br>
- [RunAPI Google provider comparison](https://runapi.ai/providers/google.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Code] <br>
**Output Format:** [Markdown with inline shell commands and SDK package names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference request JSON files, RunAPI task IDs, and RunAPI authentication configuration.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
