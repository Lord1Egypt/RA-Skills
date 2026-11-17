## Description:

CLI skill for Telegram to sync chats, search messages, filter keywords, and monitor groups from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackwener](https://clawhub.ai/user/jackwener)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to operate a Telegram CLI for local-first chat sync, search, filtering, export, monitoring, and carefully confirmed message sending from the terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad access to a personal Telegram account.

Mitigation: Use a dedicated Telegram account or narrowly scoped chats where possible, and install only when that account access is acceptable.

Risk: Telegram API credentials and the Telethon session can function like account credentials.

Mitigation: Protect TG_API_ID, TG_API_HASH, and session files as secrets, and keep the local data directory private.

Risk: The skill locally caches private chat data.

Mitigation: Restrict filesystem access to the cache, prefer structured YAML or JSON output for reviewable agent use, and purge cached data when it is no longer needed.

Risk: The skill can send real Telegram messages.

Mitigation: Require manual confirmation before allowing an agent to run any tg send command.

Risk: Persistent listening or scheduled refresh can keep collecting new messages.

Mitigation: Avoid tg listen --persist and scheduler-based refresh unless continuous collection is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackwener/skills/tg-cli)
- [Publisher profile](https://clawhub.ai/user/jackwener)
- [Structured output schema](artifact/SCHEMA.md)
- [PyPI package](https://pypi.org/project/kabi-tg-cli/)
- [Telegram app credentials](https://my.telegram.org/apps)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional YAML or JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Machine-readable command output uses the envelope documented in SCHEMA.md; non-TTY stdout defaults to YAML.]

## Skill Version(s):

0.4.1 (source: server release, changelog, pyproject.toml; SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
