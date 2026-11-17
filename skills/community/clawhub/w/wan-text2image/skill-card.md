## Description:

Uses Alibaba Cloud DashScope's Wan2.6 text-to-image model to generate images from text prompts through a shell script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baokui](https://clawhub.ai/user/baokui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to call Alibaba Cloud DashScope Wan2.6-t2i for text-to-image generation from positive prompts, optional negative prompts, and supported image sizes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Alibaba DashScope using the user's configured API key.

Mitigation: Use the skill only when sending prompt content to DashScope is acceptable, and avoid including secrets or sensitive data in prompts.

Risk: Prompt, negative prompt, and size arguments are passed into the JSON request by the shell script, and size validation is not enforced by the script.

Mitigation: Use trusted inputs, add JSON-safe request encoding before accepting untrusted text, and restrict size to documented values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baokui/skills/wan-text2image)
- [Alibaba DashScope multimodal generation endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands; the invoked API returns JSON containing generated image data or a URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY and curl; documented image sizes are 1280*1280, 720*1280, and 1280*720.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
