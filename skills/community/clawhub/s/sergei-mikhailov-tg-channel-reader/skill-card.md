## Description: <br>
Read posts and comments from Telegram channels via MTProto (Pyrogram or Telethon), including recent messages and discussion replies from public or private channels by time window. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bzsega](https://clawhub.ai/user/bzsega) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent fetch, inspect, and summarize Telegram channel posts, comments, and channel metadata for channels visible to the user's Telegram account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Telegram credentials and local session files that can grant access to channels visible to the user's Telegram account. <br>
Mitigation: Install only when this access is intended, protect TG_API_HASH and session files like account credentials, and avoid sharing or syncing session files. <br>
Risk: Fetching with output files or unread tracking can retain Telegram channel data or reading history on disk. <br>
Mitigation: Use output and read-unread options only when local retention is intended, and manage generated files according to the user's data handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bzsega/sergei-mikhailov-tg-channel-reader) <br>
- [Telegram API development tools](https://my.telegram.org) <br>
- [OpenClaw Control UI documentation](https://docs.openclaw.ai/web/control-ui) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI commands return JSON or plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write fetched channel data or read-state files locally when output or unread-tracking options are used.] <br>

## Skill Version(s): <br>
0.9.4 (source: server release metadata, CHANGELOG, setup.py; released 2026-05-16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
