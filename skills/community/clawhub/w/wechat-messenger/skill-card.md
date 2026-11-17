## Description:

Send WeChat messages via direct Win32 API in about two seconds per message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen6896qqwee](https://clawhub.ai/user/chen6896qqwee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to send a specified message to a named WeChat contact from a logged-in Windows WeChat desktop session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can take over the active Windows desktop session and send real WeChat messages without confirmation or recipient verification.

Mitigation: Test with non-sensitive messages first, keep the desktop idle while it runs, avoid ambiguous contact names, and add confirmation, recipient verification, clipboard cleanup, and pinned dependencies before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chen6896qqwee/skills/wechat-messenger)

## Skill Output:

**Output Type(s):** [shell commands, text, guidance]

**Output Format:** [Command-line invocation and plain-text status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a running, logged-in Windows WeChat PC session with pywin32 and pyperclip installed.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
