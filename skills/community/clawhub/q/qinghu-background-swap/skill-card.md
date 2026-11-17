## Description:

智能识别商品主体，一键替换图片背景，生成不同风格的营销场景图，无需 PS。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

电商运营者和商品内容创作者可用它将商品图替换为指定营销场景，快速生成多种背景版本。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images are uploaded to Qinghu, and generation uses the user's account and may incur charges.

Mitigation: Use only images you are comfortable sending to Qinghu and account for generation charges before creating images.

Risk: An exposed API key could allow unintended account access.

Mitigation: Keep the API key private and avoid sharing it in prompts or output.

Risk: The security review covers the supplied instructions, not the external CLI package implementation.

Mitigation: Pin a reviewed CLI version and inspect update commands before execution.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [ClawHub release page](https://clawhub.ai/autoagc/skills/qinghu-background-swap)

## Skill Output:

**Output Type(s):** [Image files, Shell commands, Guidance]

**Output Format:** [Generated image files with concise text and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated edits may slightly change product details; review text, logos, and product structure.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
