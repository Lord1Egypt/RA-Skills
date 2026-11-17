## Description:

Read-only Telegram CLI via MTProto that lists chats, fetches messages, downloads media, and manages local Telegram accounts and sessions without sending messages or modifying Telegram data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberash-dev](https://clawhub.ai/user/cyberash-dev)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to read Telegram chats, fetch message history, download message media, and automate Telegram data extraction through a local MTProto CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned global third-party CLI that handles Telegram credentials, session keys, private messages, and downloaded media.

Mitigation: Before installing, verify the package and source, prefer a pinned or isolated install, and use an account and environment where exposure of Telegram data would have acceptable impact.

Risk: Telegram session files and API credentials are sensitive local authentication material.

Mitigation: Do not read, copy, log, or expose session files or api_id/api_hash values; keep keychain and session storage protected.

Risk: Downloaded Telegram media can contain private or sensitive content.

Mitigation: Download only to an intended output directory and review local access, retention, and sharing controls for the saved files.

## Reference(s):

- [tg-mtproto-cli npm package](https://www.npmjs.com/package/tg-mtproto-cli)
- [tg-mtproto-cli source repository](https://github.com/cyberash-dev/tg-mtproto-cli)
- [Telegram API application credentials](https://my.telegram.org/apps)
- [ClawHub skill page](https://clawhub.ai/cyberash-dev/skills/tg-mtproto-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may produce JSON output or downloaded media when run with the tg CLI.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
