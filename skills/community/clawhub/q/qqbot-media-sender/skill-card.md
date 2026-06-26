## Description: <br>
One-click sending of images, videos, and files to QQ chat windows, with batch sending and optional automatic compression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bg1avd](https://clawhub.ai/user/bg1avd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QQBot users can use this skill to prepare local image, video, and document sends to QQ chats or groups. It is suited for batch media sharing workflows where file type detection, size checks, delay control, and generated QQ media tags are useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Accidental sharing of the wrong local files or QQ recipient. <br>
Mitigation: Use explicit file paths, review wildcard or directory matches before sending, verify the QQ chat or group target, and avoid broad workspace, home, temporary, or document folders that may contain private data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bg1avd/qqbot-media-sender) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text and QQ media/file tags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates absolute-path QQ media tags after checking local file existence and enforcing a 20 MB file size limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
