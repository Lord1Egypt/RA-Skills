## Description:

为商品图片批量添加品牌 logo 或版权文字水印，支持位置、透明度和大小控制，并使用本地 ImageMagick 或 ffmpeg 处理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operators use this skill to add brand logo or copyright watermarks to single images or batches of product images while controlling placement, opacity, and scale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch file patterns could select unintended images for watermarking.

Mitigation: Review file globs and generate one sample image for position and opacity confirmation before running batch commands.

Risk: ImageMagick may be missing and installation commands use the local system package manager.

Mitigation: Confirm the package manager command with the user before installing dependencies.

Risk: Local image-processing commands can overwrite or create files on disk.

Mitigation: Write processed images to a separate output directory and preserve original source images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-image-watermark-add)
- [@iqinghu/qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides ImageMagick and ffmpeg recipes that may create watermarked image files in a local output directory.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
