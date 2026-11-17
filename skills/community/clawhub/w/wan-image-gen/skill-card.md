## Description:

wan-image-gen uses Alibaba Cloud Model Studio DashScope Wan image generation models to submit text-to-image jobs, poll task status, and download generated images locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouweico](https://clawhub.ai/user/zhouweico)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate images from text prompts, choose cost or quality tiers, run dry-run request previews, poll existing image-generation tasks, and save completed PNG outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A changed baseUrl, DASHSCOPE_BASE_URL, or config.json can cause the DashScope API key to be sent to an unintended endpoint.

Mitigation: Keep the base URL pinned to the legitimate DashScope endpoint, prefer DASHSCOPE_API_KEY from the environment, and avoid letting untrusted projects write config.json or environment variables.

Risk: Generated image URLs are downloaded as remote files without independent content validation.

Mitigation: Run the skill in a network- and disk-limited workspace, store outputs in a dedicated directory, and review downloaded files before reuse.

## Reference(s):

- [Wan Image Generation API Notes](references/api.md)
- [Alibaba Cloud Model Studio Text-to-Image V2 API](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)
- [Alibaba Cloud Model Studio Text-to-Image](https://help.aliyun.com/zh/model-studio/text-to-image)
- [Alibaba Cloud Model Studio Regions](https://help.aliyun.com/zh/model-studio/regions/)
- [ClawHub skill page](https://clawhub.ai/zhouweico/skills/wan-image-gen)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands; runtime output is plain text, dry-run JSON, task identifiers, file paths, and PNG image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=18 and DASHSCOPE_API_KEY; supports prompt, model, tier, goal, ratio, size, seed, polling, timeout, and output directory options.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
