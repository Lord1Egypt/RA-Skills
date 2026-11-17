## Description:

检测到抖音、快手、小红书、B站、微博、西瓜视频等平台链接时，自动解析并下载无水印视频，直接发送文件给用户。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sjzai](https://clawhub.ai/user/sjzai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to detect supported short-video platform links in chat, parse them through a third-party service, and return a downloaded watermark-free video file or link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supported video links are sent to an external parsing API.

Mitigation: Use explicit user confirmation and scoped network permissions before sending private or sensitive links to the parser.

Risk: Downloaded files are stored on a publicly reachable HTTP server.

Mitigation: Use HTTPS, random or signed download URLs, quotas, cleanup, and host and size validation before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sjzai/skills/qushuiyin)

## Skill Output:

**Output Type(s):** [text, files, shell commands]

**Output Format:** [Status text plus a video file or public download link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns SUCCESS or FAIL status from the download script; successful runs include a file path, file size, and public video URL.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
