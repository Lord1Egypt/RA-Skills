## Description:

智能擦除商品图片中的人物、水印、文字及杂物，并自动补全背景，完成商品修图与素材优化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External users working with product images use this skill to remove selected people, watermarks, text, or clutter and fill the area with a generated background.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI updates and tool-returned instructions can influence shell commands.

Mitigation: Preinstall a reviewed, fixed CLI version, and review upgrades and commands supplied in tool messages before execution.

Risk: Images are uploaded to Qinghu for processing, which consumes account credits.

Mitigation: Tell users about the upload and credit use before processing their images.

## Reference(s):

- [Clawhub skill release](https://clawhub.ai/autoagc/skills/qinghu-image-eraser)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Guidance, Shell commands]

**Output Format:** [Edited image files with Markdown guidance and shell commands using JSON arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generative edits can alter product details; review important text, logos, and product structure in the result.]

## Skill Version(s):

0.1.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
