## Description: <br>
Generate and edit video with Wan through RunAPI, using the RunAPI CLI for one-off generation and SDKs for app or backend integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to route Wan video and image generation or editing tasks through RunAPI. It provides CLI guidance for one-off tasks and SDK package guidance for application integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, uploaded media, and generation requests are sent to RunAPI. <br>
Mitigation: Use the skill only when RunAPI/Wan is intended, and avoid sending sensitive prompts or media unless that use is permitted by the user's policy. <br>
Risk: Authentication may rely on RUNAPI_API_KEY, runapi login, or saved CLI configuration. <br>
Mitigation: Prefer a scoped RunAPI account or API key for this workflow and avoid exposing credentials in shared logs, prompts, or configuration files. <br>


## Reference(s): <br>
- [RunAPI Wan homepage](https://runapi.ai/models/wan) <br>
- [RunAPI Wan model documentation](https://runapi.ai/models/wan.md) <br>
- [RunAPI Alibaba provider comparison](https://runapi.ai/providers/alibaba.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and package names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference the runapi CLI, RUNAPI_API_KEY, saved CLI authentication, and RunAPI SDK package names.] <br>

## Skill Version(s): <br>
0.2.4 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
