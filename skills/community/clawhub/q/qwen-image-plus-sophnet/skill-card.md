## Description: <br>
Generate images via Sophnet Qwen-Image-Plus and poll for task completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DuffyCoder](https://clawhub.ai/user/DuffyCoder) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to request image generation from Sophnet Qwen-Image-Plus, poll the task until it succeeds, and return generated image URLs to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and negative prompts are sent to Sophnet for image generation. <br>
Mitigation: Avoid sensitive, regulated, or confidential prompt content unless sharing it with Sophnet is approved for the use case. <br>
Risk: API keys may be exposed if passed directly as command-line arguments. <br>
Mitigation: Use a scoped Sophnet API key and provide it through the SOPHNET_API_KEY environment variable. <br>
Risk: Generated image URLs may include signature or access query parameters. <br>
Mitigation: Treat generated URLs as shareable access links and avoid broad redistribution. <br>


## Reference(s): <br>
- [Qwen Image Plus Sophnet ClawHub release](https://clawhub.ai/DuffyCoder/qwen-image-plus-sophnet) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text status lines and image URL lines, with Markdown or shell-command guidance when used by an agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Sophnet API key and returns one or more IMAGE_URL values after task completion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
