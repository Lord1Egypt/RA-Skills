## Description:

根据小红书文章内容自动生成配图。使用PIL将文章标题、副标题、内容生成在图片上，适合小红书笔记配图。

This skill is ready for commercial/non-commercial use.

## Publisher:

[binsonhao](https://clawhub.ai/user/binsonhao)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agents use this skill to generate Xiaohongshu-style cover images from a title, optional subtitle, and optional multiline article content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated output is saved to a fixed local file path, so rerunning the script can replace the previous image.

Mitigation: Move or rename the generated xhs_cover.jpg file before rerunning when multiple images need to be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binsonhao/skills/redbook-image-generator)

## Skill Output:

**Output Type(s):** [Files, Shell commands]

**Output Format:** [JPEG image file with command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the generated image to xhs_cover.jpg at a fixed local output path.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
