## Description:

Toggle-enabled skill that fetches Telegram message history at session start for conversational continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fourthdensity](https://clawhub.ai/user/fourthdensity)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to maintain continuity in Telegram-based agent conversations by fetching recent current-chat messages when a session starts or when manually requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recent Telegram messages may be added to the agent context and sent to the configured LLM provider.

Mitigation: Use manual fetch or a low fetch count for sensitive chats, and disable the skill when continuity is not needed.

Risk: Auto-fetch can expose more chat history than needed for a task.

Mitigation: Keep auto-fetch off for sensitive conversations and request only the number of messages needed for the current task.

## Reference(s):

- [Telegram Context ClawHub page](https://clawhub.ai/fourthdensity/skills/telegram-context)
- [OpenClaw skills homepage](https://github.com/openclaw/skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and plain-text agent responses with command status, fetched-message context summaries, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the current Telegram chat only; fetch count is user-controlled and defaults to 20 messages.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
