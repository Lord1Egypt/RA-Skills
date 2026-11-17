## Description:

集合四大高频实用图像工具：去水印/OCR文字识别/图片压缩/标准证件照生成。一站式解决日常图片处理需求。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to process images through four local Python tools: watermark removal, OCR text extraction, image compression, and standard ID photo generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install unpinned Python packages and download OCR or background-removal model files, changing the user's Python environment.

Mitigation: Review and pin dependencies before use, run the tools in a virtual environment or container, and require explicit approval before package installation or model downloads.

Risk: The watermark-removal workflow can be used on images the user is not authorized to modify.

Mitigation: Use watermark removal only for images where the user has the rights or permission to edit the content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/toolbox-10-skill)
- [Publisher profile](https://clawhub.ai/user/bettermen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and JSON-producing Python script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scripts can write processed image files and OCR text or JSON files to user-selected output paths.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
