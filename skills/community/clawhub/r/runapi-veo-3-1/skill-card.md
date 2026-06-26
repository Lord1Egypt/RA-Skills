## Description: <br>
Generate and edit video with Veo 3 through RunAPI, using the CLI for one-off agent tasks and SDK guidance for application or backend integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route agent requests for Veo 3 video generation, editing, extension, or upscaling through the RunAPI CLI. Developers integrating RunAPI into an application or backend can use the SDK package guidance instead. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can involve external RunAPI CLI calls and account authentication. <br>
Mitigation: Install and authenticate the RunAPI CLI only when intending to use RunAPI for Veo video generation or editing. <br>
Risk: Prompts, images, videos, and API credentials may be sensitive. <br>
Mitigation: Review RunAPI pricing, account controls, and data handling before submitting media or prompts, and avoid placing API keys in shared files or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runapi-ai/runapi-veo-3-1) <br>
- [RunAPI Veo 3.1 model overview](https://runapi.ai/models/veo-3.1) <br>
- [RunAPI Veo 3.1 documentation](https://runapi.ai/models/veo-3.1.md) <br>
- [RunAPI Google provider comparison](https://runapi.ai/providers/google.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and package names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce CLI request guidance for synchronous or asynchronous video tasks.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
