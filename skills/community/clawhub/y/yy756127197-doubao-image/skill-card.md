## Description:

使用字节跳动豆包 Doubao SeeDream 模型生成高质量图片。支持文生图、AI 绘图、插画创作等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yy756127197](https://clawhub.ai/user/yy756127197)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate image assets from text prompts through the Volcengine ARK API and Doubao SeeDream model. It helps an agent suggest commands, configure required environment variables, call the generation scripts, and save generated images locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and an ARK API bearer token are sent to Volcengine/Doubao during image generation.

Mitigation: Use the skill only when that external data transfer is acceptable, keep credentials out of project files and shell history, and rotate tokens if exposure is suspected.

Risk: Diagnostics and troubleshooting guidance may reveal sensitive credential prefixes in shared logs.

Mitigation: Avoid running diagnostics in shared logs until the API-key-prefix output is fixed, and redact environment output before sharing.

Risk: Automatic trigger phrases may initiate image generation before the user has reviewed the external API call.

Mitigation: Require explicit confirmation before auto-triggered generation sends prompts or credentials to the provider.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yy756127197/skills/yy756127197-doubao-image)
- [Volcengine ARK documentation](https://www.volcengine.com/docs/82379)
- [Doubao product page](https://www.volcengine.com/product/doubao)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell and Python commands; generated PNG image files saved to a local output directory.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ARK_API_KEY and supports prompt, size, watermark, output directory, timeout, and retry settings.]

## Skill Version(s):

2.0.0 (source: server release metadata, skill metadata, and changelog released 2026-04-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
