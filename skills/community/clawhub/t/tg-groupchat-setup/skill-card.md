## Description:

Configure a MoltBot agent to participate in a Telegram group chat by adding the group to the allowlist, setting mention patterns, and configuring sender permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arekqq](https://clawhub.ai/user/arekqq)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure a MoltBot Telegram integration for group chats, including group allowlisting, mention gating, and allowed sender setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script reads the local MoltBot gateway config and uses the Telegram bot token; the security scan reports unsafe handling that could allow unintended local code execution.

Mitigation: Review before installing, run only in a trusted local environment, and fix the helper script to pass the config path and API response as data rather than interpolating them into Python source.

Risk: Disabling Telegram privacy mode allows the bot to receive all group messages.

Mitigation: Use `requireMention: true`, keep `groupAllowFrom` restricted to approved senders, and add the bot only to intended groups.

Risk: The setup patches gateway configuration and restarts the gateway.

Mitigation: Review the proposed configuration merge before applying it and preserve existing allowed users and mention patterns.

## Reference(s):

- [Telegram Bot Privacy Mode](references/telegram-privacy-mode.md)
- [ClawHub skill page](https://clawhub.ai/arekqq/skills/tg-groupchat-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Telegram group ID and the Telegram user IDs or usernames allowed to trigger the bot.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
