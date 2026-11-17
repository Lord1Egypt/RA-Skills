## Description:

使用 Seedream 5.0 Lite 精修授权商品照片，修复灰尘、划痕、褶皱、反光、边缘和背景瑕疵，同时保持商品结构、材质、标签与商业事实不变。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retouch authorized product photos for ecommerce and product presentation while preserving product facts such as structure, materials, labels, color, quantity, and certification details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the helper trusts server-provided upload and download locations too broadly.

Mitigation: Review upload and result download URLs before use with confidential product photos or in sensitive network environments, and use only selected images intended for AI Hive processing.

Risk: The workflow sends selected product images and prompts to AI Hive and may store an API key locally.

Mitigation: Use non-confidential authorized product images, manage the AI_HIVE_API_KEY or local config file carefully, and keep local key file permissions restricted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedream-5-lite-product-retouch)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and generated image files downloaded by the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed Seedream 5.0 Lite image model through AI Hive, requires at least one input product image, and can save an API key locally with 0600 permissions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
