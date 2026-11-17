## Description:

Let your agent read and monitor Telegram channels: fetch posts, captions, link previews, and comments from public or private channels and turn them into daily digests, summaries, and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bzsega](https://clawhub.ai/user/bzsega)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to read Telegram channels they can access and turn recent posts, captions, link previews, and comments into digests, summaries, monitoring updates, and alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Telegram account session that can read private channels available to that account.

Mitigation: Install only where that account access is acceptable, keep session and backup files private, and use a dedicated environment with reviewed dependency versions.

Risk: Telegram login codes, 2FA passwords, and auth progress can be exposed if handled through logged or shared channels.

Mitigation: Prefer self-authentication or stdin, avoid /tmp code or password files when possible, and avoid using Telethon auth output in logged environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bzsega/skills/sergei-mikhailov-tg-channel-reader)
- [Telegram API credentials portal](https://my.telegram.org)
- [OpenClaw Control UI documentation](https://docs.openclaw.ai/web/control-ui)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON or plain text from the Telegram reader CLI, with Markdown setup and usage guidance in the skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write fetched channel data to JSON files when the user requests file output.]

## Skill Version(s):

0.11.1 (source: server release metadata, artifact changelog, setup.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
