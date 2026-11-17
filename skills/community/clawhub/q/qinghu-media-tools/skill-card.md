## Description:

帮助电商卖家通过青虎AI处理视频去水印、去字幕和画质提升，并引导图片编辑、压缩及加水印任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce sellers and content creators use this skill to improve product media, remove video subtitles or watermarks, upscale videos, and route image-editing requests to specialized tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency setup may install or update Node.js and qhkit command-line software.

Mitigation: Review and authorize installations before running the skill.

Risk: Selected media files may be uploaded for processing, and the service requires an API token.

Mitigation: Upload only approved media and keep the API token private.

Risk: Removing watermarks from media without permission may infringe rights.

Mitigation: Use watermark-removal features only on media you have rights to modify.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-media-tools)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Text with command examples and links to processed media]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report processing status, media URLs, and credits charged.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
