## Description:

帮助用户通过青虎AI批量移除视频水印并获取处理后的视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

用户使用青虎AI处理自有或获授权的视频，批量去除水印或角标，并获取处理结果。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local videos are uploaded to a third-party cloud service for processing.

Mitigation: Confirm that the user is comfortable sharing each video with 青虎AI before uploading.

Risk: The workflow needs an API token and installs a third-party npm CLI.

Mitigation: Protect the token, review the package and version before installation, and avoid unnecessary persistent PATH changes.

Risk: Removing watermarks from others' copyrighted videos may infringe their rights.

Mitigation: Use only videos the user owns or is authorized to modify.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-video-watermark-remove)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [青虎AI API 密钥](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with commands and output video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task IDs, output video URLs, and charged credits.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
