## Description:

Generates images from text prompts with Alibaba DashScope Tongyi Wanxiang through a Node.js helper and returns a media URL or saved local file path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangshengli0421](https://clawhub.ai/user/wangshengli0421)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to generate text-to-image results when a user asks to create an image from a written description. It is intended for text-to-image generation, not image editing or style transfer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generation requests are sent to Alibaba DashScope.

Mitigation: Avoid sensitive prompt content and install only when use of Alibaba DashScope is acceptable for the intended workflow.

Risk: API keys can be passed through command-line arguments.

Mitigation: Prefer DASHSCOPE_API_KEY or configured provider credentials so secrets are less likely to appear in shell history or process listings.

Risk: The optional filename output can overwrite existing writable local files.

Mitigation: Use --filename only with a clearly safe output path and check whether the target file already exists before running the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangshengli0421/skills/tianshu-image)
- [DashScope Console](https://dashscope.console.aliyun.com/)
- [DashScope Multimodal Generation API Endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown image output backed by a MEDIA_URL or MEDIA local path emitted by a Node.js command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY or an equivalent configured provider API key; optional filename output writes the generated image to a local path.]

## Skill Version(s):

1.0.0 (source: evidence release and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
