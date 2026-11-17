## Description:

Manages Telegram group chat replies by responding to mentions, questions, name calls, technical topics, or priority users while reducing spam and bot loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zboxman](https://clawhub.ai/user/zboxman)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Telegram bot operators use this skill to define when an agent should answer in group chats and when it should remain silent. It is intended for group-message handling, bot configuration, reply-policy setup, multi-bot groups, mention handling, and bot-loop avoidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bot may reply more broadly than intended if its bot name, priority user IDs, or cooldown behavior are configured incorrectly.

Mitigation: Review those settings before deployment and test mention, question, emoji-only, other-bot, and cooldown scenarios against the intended Telegram group.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zboxman/skills/telegram-group-chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown guidance with plain-text reply decisions, including the NO_REPLY sentinel]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return exactly NO_REPLY when the bot should process a message silently without sending a chat response.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
