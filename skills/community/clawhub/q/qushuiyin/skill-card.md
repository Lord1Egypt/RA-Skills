## Description: <br>
短视频去水印下载。检测到抖音、快手、小红书、B站、微博、西瓜视频等平台链接时，自动解析并下载无水印视频，直接发送文件给用户。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sjzai](https://clawhub.ai/user/sjzai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to detect supported short-video platform links in messages, resolve watermark-free media through a third-party parsing service, and return the resulting video file or download link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video links are processed automatically and sent to a third-party parsing service. <br>
Mitigation: Require explicit user confirmation before processing links, disclose the third-party service, and validate that links belong to supported domains. <br>
Risk: Downloaded videos are stored in a publicly served directory and may be exposed through public HTTP links. <br>
Mitigation: Use private or expiring delivery links, limit file size and type, and clean up old media after delivery. <br>
Risk: Service credentials and deployment settings appear in source-level constants. <br>
Mitigation: Move credentials and deployment-specific paths or hosts into protected runtime configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sjzai/qushuiyin) <br>
- [Third-party video parsing API endpoint](https://qyapi.ipaybuy.cn/api/video) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Plain text status strings, local video files, and public download URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns SUCCESS or FAIL-prefixed status text; successful runs include a local media path, file size, and public URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
