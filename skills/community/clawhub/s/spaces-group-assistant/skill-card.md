## Description:

Spaces Group Assistant extends a Telegram/OpenClaw assistant with trusted group access to workspace knowledge, memory, logs, skills, and analytics while blocking calendar requests outside private chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helladventurer](https://clawhub.ai/user/helladventurer)

### License/Terms of Use:

MIT

## Use Case:

Trusted teams or communities use this skill to let a Telegram assistant answer from local workspace knowledge, memory, logs, and analytics in a designated group or private chat. It is intended for environments where participants are already trusted with the assistant's workspace context, while calendar access remains private-chat only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad workspace, memory, log, and possible execution-hook access to all users in the configured Telegram group and to private chats without per-user authorization.

Mitigation: Install only when every configured group member and private-message user is trusted with workspace memory, logs, internal documents, and enabled execution hooks.

Risk: Calendar privacy relies on keyword-based blocking for group chats.

Mitigation: Add tool-level calendar authorization and blocking before broader deployment instead of relying only on keyword filtering.

Risk: The server-side security verdict is suspicious due to broad trust assumptions.

Mitigation: Add explicit user allowlists and per-tool authorization before using the skill outside a tightly trusted team context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/helladventurer/skills/spaces-group-assistant)
- [Publisher Profile](https://clawhub.ai/user/helladventurer)
- [Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Telegram assistant text or Markdown-style responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calendar-related requests are blocked outside private chats; trusted group and private chats pass non-calendar requests to the host assistant.]

## Skill Version(s):

0.1.2 (source: evidence.release.version and target metadata; artifact package.json is 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
