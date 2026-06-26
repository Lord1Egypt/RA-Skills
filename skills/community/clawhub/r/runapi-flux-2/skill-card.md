## Description: <br>
Generate and edit images with Flux 2 through RunAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to ask an agent to generate, edit, or transform images with Flux 2 through RunAPI. The skill is oriented around one-off CLI use, with SDK guidance for application integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, request files, and input images may be sent to a third-party image-generation service. <br>
Mitigation: Review RunAPI data-handling requirements before using confidential content, and avoid sending sensitive inputs unless approved for that environment. <br>
Risk: The skill can use API-key or saved CLI authentication. <br>
Mitigation: Review how the runapi CLI stores login sessions or API keys and handle RUNAPI_API_KEY as a sensitive credential. <br>


## Reference(s): <br>
- [RunAPI Flux 2 model page](https://runapi.ai/models/flux-2) <br>
- [RunAPI Flux 2 model documentation](https://runapi.ai/models/flux-2.md) <br>
- [Black Forest Labs provider comparison](https://runapi.ai/providers/black-forest-labs.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [ClawHub skill page](https://clawhub.ai/runapi-ai/runapi-flux-2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with inline shell commands and JSON request-file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or retrieve image-generation outputs through the RunAPI CLI; authentication can use RUNAPI_API_KEY, runapi login, or saved CLI configuration.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
