## Description:

Control Discord via Clawdbot to send messages, manage reactions, stickers, emojis, polls, threads, pins, search, information lookups, and moderation in channels or DMs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fresh3](https://clawhub.ai/user/fresh3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a configured Clawdbot Discord integration for routine Discord messaging, collaboration, content upload, search, information lookup, and permission-gated moderation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to read, post, delete, and upload content in Discord.

Mitigation: Install it only where the Clawdbot Discord permissions match the intended use, and disable unneeded action groups such as messages, search, uploads, roles, and moderation.

Risk: Moderation, deletion, direct-message, and local-file upload actions can affect users or expose content if used without review.

Mitigation: Require explicit operator review before deleting messages, moderating users, sending DMs, or uploading local files.

## Reference(s):

- [ClawHub Discord skill page](https://clawhub.ai/fresh3/skills/taizi-discord)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with JSON action examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes Discord action payloads and permission-gating notes for messages, uploads, roles, and moderation.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
