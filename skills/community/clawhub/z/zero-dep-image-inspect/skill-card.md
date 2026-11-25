## Description:

无需 Pillow 或 OpenCV，即可用 Python 标准库分析 PNG 图像并生成裁切、缩放和对照结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

面向开发者和设计人员，用于检查 PNG 图片的亮度、主色和清晰度线索，裁切或缩放图像，并制作并排对照图或联系表。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill also includes a browser text-size adjustment example, which may extend beyond its image-diagnosis description.

Mitigation: Review that example before use and apply any page adjustment only to the user-designated text element.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/oracis/skills/zero-dep-image-inspect)

## Skill Output:

**Output Type(s):** [Analysis, Files, Code, Shell commands, Guidance]

**Output Format:** [CLI text summaries, PNG image files, and Markdown with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image measurements are diagnostic proxies. PNG support is limited to 8-bit non-interlaced images; JPEG input must first be converted to PNG.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
