## Description:

视频批量加 logo/水印。递归扫描目录或处理单个视频，用 ffmpeg 把图片 logo（PNG/JPG）或文字水印（Pillow 渲染，支持中文）叠加到固定位置，标识来源版权、防盗用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjbook](https://clawhub.ai/user/bjbook)

### License/Terms of Use:

MIT-0

## Use Case:

Video creators, course producers, and teams use this skill to add image or text watermarks to individual videos or batches of videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional replacement mode may delete originals or overwrite another video.

Mitigation: Keep backups, preview the batch, and use a separate output folder outside the source directory. Avoid --replace until destination collision checks and failure-safe replacement are implemented.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bjbook/skills/zhz-video-logo)
- [Publisher profile](https://clawhub.ai/user/bjbook)
- [Project homepage](http://openclaw.bjbook.net/)

## Skill Output:

**Output Type(s):** [Video files, Command-line instructions, Guidance]

**Output Format:** [Watermarked video files and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video output format follows the input container where supported; other inputs may be written as MP4 or MKV.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
