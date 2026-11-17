## Description:

Automatically monitors configured Telegram group messages that mention the bot and forwards the message text to a configured QQ private chat through OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bg1avd](https://clawhub.ai/user/bg1avd)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to bridge Telegram group mentions into QQ private messages for approved accounts and recipients. It is intended for configured Telegram groups, QQ targets, and OpenClaw session files where message relay is explicitly permitted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose private OpenClaw session content when configured to read Telegram session JSONL files.

Mitigation: Use it only with approved Telegram groups and QQ recipients, configure a dedicated session file, and restrict file permissions to the OpenClaw runtime account.

Risk: Telegram message text and configuration values reach shell command construction in the current implementation.

Mitigation: Do not deploy it with untrusted Telegram senders until command execution uses execFile or spawn argument arrays and validates the account, target, group, and session path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bg1avd/skills/telegram-qq-bridge)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Skill Development Guide](https://docs.openclaw.ai/skills/develop)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text forwarded messages and Markdown setup guidance with JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forwarding depends on a configured Telegram session file, QQ account, QQ target, and bot mention trigger.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact config, and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
