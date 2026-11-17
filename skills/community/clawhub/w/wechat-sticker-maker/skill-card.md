## Description:

微信表情包制作工具。自动将六宫格、九宫格、十二宫格的原图裁剪并转换为符合微信表情包规范的格式（表情主图 240x240，聊天页图标 50x50）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[guanyang](https://clawhub.ai/user/guanyang)

### License/Terms of Use:


## Use Case:

External creators and agent users use this skill to turn grid-based source images into WeChat sticker-pack draft assets, including resized PNG stickers, icon images, and editable metadata templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runner creates a local Python environment and installs unpinned dependencies from the network.

Mitigation: Review and pin dependencies before deployment, or run installation in a contained workspace with trusted package indexes.

Risk: Untrusted images or very large layout values can increase file generation, CPU, and memory use.

Mitigation: Process trusted images, set a dedicated output directory, and use reasonable explicit layout values.

Risk: Background removal adds model/runtime processing and may produce imperfect edges on complex images.

Mitigation: Use transparent source PNGs when possible, enable --remove-bg only when needed, and manually review generated sticker assets before submission.

## Reference(s):

- [WeChat Sticker Open Platform](https://sticker.weixin.qq.com/)
- [WeChat Sticker Making Specifications](https://sticker.weixin.qq.com/cgi-bin/mmemoticon-bin/readtemplate?t=guide/index.html#/makingSpecifications#specifications_stickers)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Configuration, Guidance]

**Output Format:** [PNG image files, text metadata templates, and Markdown or shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates main and icon output directories, meta.txt, info.txt, and candidate cover/icon PNG files in the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
