## Description:

Long-term Telegram memory for AI agents — search conversations, get digests, extract decisions. Connects to any Telegram channel via user's own account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[may4vfx](https://clawhub.ai/user/may4vfx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent search synced Telegram conversations, summarize channel activity, extract decisions and action items, manage connected sources, and check account balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects Telegram content to a third-party memory service and can index selected channels or groups.

Mitigation: Use it only for Telegram sources the user intentionally chooses, keep scopes narrow, and confirm how to revoke the Telegram connection or delete synced data before relying on it.

Risk: The skill requires an Agent Memory API key that grants access to the external service.

Mitigation: Treat AGENT_MEMORY_API_KEY as a secret, store it in a safer secret store when available, avoid pasting it into normal chat, and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/may4vfx/skills/telegram-agent-memory)
- [Publisher profile](https://clawhub.ai/user/may4vfx)
- [Agent Memory Telegram bot](https://t.me/AgentMemoryBot)
- [Agent Memory API base URL](https://agent.ai-vfx.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with inline bash curl commands and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and the AGENT_MEMORY_API_KEY environment variable.]

## Skill Version(s):

0.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
