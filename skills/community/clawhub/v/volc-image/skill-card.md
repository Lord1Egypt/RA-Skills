## Description:

火山引擎图像生成 - 使用火山引擎方舟API生成图片并下载.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magiesky](https://clawhub.ai/user/magiesky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate images from text prompts through the Volcengine Ark API and save the returned image locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts are sent to Volcengine.

Mitigation: Avoid sensitive prompts and use the skill only where sending prompt content to Volcengine is acceptable.

Risk: The Volcengine API key can be mishandled if passed directly on the command line.

Mitigation: Set ARK_API_KEY as an environment variable or secret instead of passing credentials as command arguments.

Risk: Generated image files are downloaded and saved locally.

Mitigation: Review the save location and consider URL validation and download timeouts before automated use.

## Reference(s):

- [Volcengine Ark Console](https://console.volcengine.com/ark/endpoint)
- [Volcengine Ark Image Generation API endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations)
- [ClawHub skill page](https://clawhub.ai/magiesky/skills/volc-image)

## Skill Output:

**Output Type(s):** [text, shell commands, code, files, guidance]

**Output Format:** [Markdown guidance with shell and Python examples; generated image files are saved locally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ARK_API_KEY and sends prompts to Volcengine; generated image URLs may be temporary.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
