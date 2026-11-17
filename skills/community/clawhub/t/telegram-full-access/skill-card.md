## Description:

Give OpenClaw full access to Telegram through a user-owned session, with options for a hosted Chiho.ai CRM flow or a self-hosted local tgchats runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seichris](https://clawhub.ai/user/seichris)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect OpenClaw or compatible agents to Telegram through an explicit user-owned login, enabling account-level chat automation and CRM-style chat management. It is intended for workflows where bot-only Telegram access is too limited.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected Telegram account grants broad read/write access to chats available to that account.

Mitigation: Use a dedicated Telegram account with limited chat membership where possible, and require explicit user approval before enabling write-capable message workflows.

Risk: Chiho Agent Access tokens can expose the connected Telegram session if leaked.

Mitigation: Protect and rotate the token, send it only as a bearer header, and do not paste it into URLs or OAuth credential fields.

Risk: The self-hosted setup asks users to run external code that handles sensitive Telegram API credentials and local session data.

Mitigation: Pin the GitHub repository to a reviewed commit and use locked dependency installation before running npm scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seichris/skills/telegram-full-access)
- [telegram-for-ai-agents on GitHub](https://github.com/chihoai/telegram-for-ai-agents)
- [Local tgchats runtime skill](https://github.com/chihoai/telegram-for-ai-agents/blob/main/skills/tgchats-local/SKILL.md)
- [Telegram workflow catalog](https://github.com/chihoai/telegram-for-ai-agents/blob/main/docs/SKILL_CATALOG.md)
- [Chiho.ai signup](https://chiho.ai/signup)
- [Chiho Agent Access](https://chiho.ai/profile/agent-access)
- [Telegram API app credentials](https://my.telegram.org/apps)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes hosted bearer-token setup guidance, local environment variable guidance, and runtime selection guidance.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
