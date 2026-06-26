## Description: <br>
Send local files, images, audio, video, and other media through QQBot end to end. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zykkk-power](https://clawhub.ai/user/zykkk-power) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send local files or URL media through QQBot by staging eligible local files and emitting QQ rich-media tags for delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user may unintentionally send sensitive local files through QQBot. <br>
Mitigation: Confirm the exact file path and intended recipient before sending. <br>
Risk: Staged copies may remain in ~/.openclaw/media/qqbot/ after delivery. <br>
Mitigation: Periodically clean the QQBot media relay directory, especially after sending sensitive files. <br>


## Reference(s): <br>
- [QQBot Send ClawHub page](https://clawhub.ai/zykkk-power/qqbot-send) <br>
- [Publisher profile](https://clawhub.ai/user/zykkk-power) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and QQ rich-media tags] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stages local files up to 10 MB into ~/.openclaw/media/qqbot/ before sending.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
