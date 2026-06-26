## Description: <br>
Uses VolcEngine's AI video API to generate videos from text prompts and query video generation task status and results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZzBpaq123](https://clawhub.ai/user/ZzBpaq123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to submit text-to-video prompts to VolcEngine and retrieve generated video task results through an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VolcEngine API credentials can be exposed if config.json is shared or committed with real keys. <br>
Mitigation: Keep config.json private, store real keys outside shared repositories when possible, and rotate keys if they are exposed. <br>
Risk: Video prompts and task identifiers are sent to a third-party API and may contain sensitive, personal, regulated, or confidential content. <br>
Mitigation: Avoid sending sensitive content to VolcEngine unless it is approved for that service and use case. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Plain text and JSON API responses containing task IDs, task status, and video URLs when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VolcEngine access_key and secret_key configuration; sends prompts and task IDs to VolcEngine.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
