## Description:

Windows desktop WeChat message automation that uses keyboard simulation to send messages to specified contacts or groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangpuego123](https://clawhub.ai/user/zhangpuego123)

### License/Terms of Use:

MIT-0

## Use Case:

People who use WeChat on Windows can ask an agent to send a single message or step through a batch of messages to named contacts or groups using the local WeChat desktop client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Desktop automation can send a message to the wrong active window, contact, or group if focus changes or WeChat search resolves unexpectedly.

Mitigation: Use only in a controlled Windows session with WeChat visible, and prefer a version with recipient verification and preview or confirmation before sending.

Risk: The skill can send messages immediately as the signed-in WeChat user.

Mitigation: Review contacts and message content before each run, especially in batch mode.

Risk: Message bodies and contact names pass through local queue files and the clipboard.

Mitigation: Avoid sensitive message bodies in batch mode, clear temporary queue state when finished, and prefer clipboard cleanup after sending.

Risk: Unpinned or broad dependency ranges can change desktop automation behavior over time.

Mitigation: Pin and review dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangpuego123/skills/wechat-talk)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text and JSON status messages, with command-line usage examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces external side effects by sending WeChat messages through the local Windows desktop client.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
