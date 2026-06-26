## Description: <br>
Generate and edit images with GPT Image through RunAPI, using the RunAPI CLI for one-off agent tasks and SDKs for application integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to generate, edit, and transform images with GPT Image through RunAPI. It supports one-off CLI workflows and SDK integration planning for applications or backend systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, uploaded images, masks, and related metadata are sent to RunAPI and upstream providers. <br>
Mitigation: Avoid sending confidential or personal content unless that data sharing is acceptable for the intended use case. <br>
Risk: The skill depends on an external CLI and service authentication. <br>
Mitigation: Install the RunAPI CLI from the documented source and use only credentials intended for RunAPI access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runapi-ai/runapi-gpt-image) <br>
- [RunAPI GPT Image model page](https://runapi.ai/models/gpt-image) <br>
- [RunAPI GPT Image model overview](https://runapi.ai/models/gpt-image.md) <br>
- [RunAPI OpenAI provider page](https://runapi.ai/providers/openai.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [GPT Image 1.5 text to image](https://runapi.ai/models/gpt-image/1.5-text-to-image.md) <br>
- [GPT Image 1.5 image to image](https://runapi.ai/models/gpt-image/1.5-image-to-image.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the runapi CLI and authentication through runapi login, saved CLI configuration, or RUNAPI_API_KEY.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
