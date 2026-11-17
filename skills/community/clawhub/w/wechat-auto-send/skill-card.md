## Description:

通过命令行自动控制微信向指定联系人发送文本消息，并支持自定义等待时间、倒计时和详细日志。

This skill is ready for commercial/non-commercial use.

## Publisher:

[2450550235-debug](https://clawhub.ai/user/2450550235-debug)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to send a WeChat text message to a named contact after they provide the recipient and exact message. The skill is intended for desktop automation where WeChat is already installed, logged in, and visible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic desktop control can send or paste messages to the wrong active WeChat window or contact.

Mitigation: Use explicit commands, verify the recipient and exact message before execution, keep WeChat visible, and test first with File Transfer Assistant.

Risk: Clipboard and keyboard automation can expose or send sensitive content.

Mitigation: Avoid sensitive content and do not use the desktop while the skill is running.

Risk: Batch or scheduled sends can amplify mistakes or unwanted messaging.

Mitigation: Do not enable batch or scheduled sends without additional confirmation, rate limits, and cancellation controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/2450550235-debug/skills/wechat-auto-send)
- [README.md](artifact/README.md)
- [OPENCLAW_USAGE.md](artifact/OPENCLAW_USAGE.md)
- [EXAMPLES.md](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown and command-line instructions with script output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces status messages for dependency checks, countdown, WeChat focus, contact selection, message paste, send completion, and errors.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
