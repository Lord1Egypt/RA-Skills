## Description: <br>
Generate and edit images with GPT Image 2 through RunAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runapi-ai](https://clawhub.ai/user/runapi-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to route image generation, editing, and transformation requests to GPT Image 2 through RunAPI. It guides one-off CLI use and points developers to SDK packages when integrating the model into an app or backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The RunAPI CLI may use a saved account session or API key. <br>
Mitigation: Review which account or RUNAPI_API_KEY the CLI will use before running image generation or editing commands. <br>
Risk: Prompts and source images may contain confidential or sensitive content. <br>
Mitigation: Submit confidential prompts or private images only when RunAPI's data handling is acceptable for the use case. <br>


## Reference(s): <br>
- [RunAPI GPT Image 2 model overview](https://runapi.ai/models/gpt-image-2.md) <br>
- [RunAPI GPT Image 2 homepage](https://runapi.ai/models/gpt-image-2) <br>
- [RunAPI OpenAI provider comparison](https://runapi.ai/providers/openai.md) <br>
- [RunAPI model catalog](https://runapi.ai/models.md) <br>
- [GPT Image 2 text-to-image variant](https://runapi.ai/models/gpt-image-2/text-to-image.md) <br>
- [GPT Image 2 image-to-image variant](https://runapi.ai/models/gpt-image-2/image-to-image.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell command examples and SDK package names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the runapi CLI for the CLI path; RUNAPI_API_KEY is optional because login or saved CLI configuration can authenticate the binary.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
