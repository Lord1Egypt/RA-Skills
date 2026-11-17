## Description:

Telegram Bot API operations for forum management, including creating, editing, and archiving forum topics, setting topic icons, and managing Telegram groups via the Bot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brennerspear](https://clawhub.ai/user/brennerspear)

### License/Terms of Use:


## Use Case:

Developers and operators managing OpenClaw Telegram integrations use this skill to create, configure, icon, archive, and clean up Telegram forum topics and their per-topic sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram bot tokens can be exposed when passed directly in shell commands.

Mitigation: Use a narrow bot scope, avoid passing real tokens as command-line arguments, and retrieve or inject tokens through safer local configuration or secret handling where available.

Risk: New Telegram topic sessions may inherit all installed skills by default.

Mitigation: Use a narrow skills allowlist for each topic and include only ready skills that match the topic purpose.

Risk: Incorrect topic names, chat IDs, or topic IDs can modify or archive the wrong Telegram forum topic.

Mitigation: Validate topic names and IDs before running create, edit, archive, or cleanup scripts.

Risk: Archived session history can be lost during cleanup.

Mitigation: Export and verify archived session history before deleting session records or transcripts.

## Reference(s):

- [Forum Topic Emoji IDs](references/emoji-ids.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Telegram Bot API command guidance and OpenClaw configuration steps; scripts require a bot token, chat ID, and topic inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
