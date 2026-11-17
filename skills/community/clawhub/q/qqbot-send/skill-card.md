## Description:

Send local files, images, audio, video, and other media through QQBot end to end.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zykkk-power](https://clawhub.ai/user/zykkk-power)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send user-requested local files or URL media through QQBot. It stages readable local files into the QQBot media relay directory when needed, then delivers them with QQ rich-media tagging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive files could be sent to QQBot if the path or recipient is not confirmed.

Mitigation: Confirm the file path and intended recipient before sending sensitive files.

Risk: Staged file copies may remain in the local QQBot media relay directory after delivery.

Mitigation: Periodically clean ~/.openclaw/media/qqbot/ when retained staged copies are no longer needed.

## Reference(s):

- [QQBot Send ClawHub Page](https://clawhub.ai/zykkk-power/skills/qqbot-send)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and QQ media tags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stages local files up to 10 MB into ~/.openclaw/media/qqbot/ and preserves the original file extension.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
