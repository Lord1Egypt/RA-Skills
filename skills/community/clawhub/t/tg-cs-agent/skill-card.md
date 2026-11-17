## Description:

Deploy and manage a Telegram customer service bot powered by Claude + RAG for setup, knowledge base updates, lifecycle management, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youziyouzishu](https://clawhub.ai/user/youziyouzishu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support operators use this skill to deploy a Telegram customer service agent that answers Seers Markets questions from a local markdown knowledge base and escalates unresolved or account-specific issues to a human support chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bot runs as a real Telegram account and can read and reply to all messages visible to that account.

Mitigation: Install it only on a dedicated customer-support Telegram account and add a deny-by-default chat allowlist before production use.

Risk: User messages may be sent to an external AI service without clear user scoping or consent.

Mitigation: Disclose AI and human-support processing to users, limit collection to support chats, and validate that the configured AI endpoint is approved.

Risk: The configurable Anthropic base URL could route conversations to an unintended AI endpoint.

Mitigation: Use the default Anthropic API URL unless an approved endpoint is required, and review any custom base URL before deployment.

Risk: Telegram session files and interactive login secrets can grant account access if exposed.

Mitigation: Protect and rotate the Telethon session, store credentials securely, and replace echoing secret prompts with non-echoing input.

Risk: Unpinned Python dependencies may change behavior or introduce supply-chain risk over time.

Mitigation: Pin dependency versions and scan the resolved environment before production deployment.

## Reference(s):

- [Seers Markets FAQ](references/seers-faq.md)
- [Seers Markets Platform Introduction](references/seers-platform.md)
- [Seers Markets Quick Trading](references/seers-trading.md)
- [Seers User Guide (English)](references/seers-user-guide-en.md)
- [Seers User Guide (Chinese)](references/seers-user-guide-zh.md)
- [Telegram API Credentials](https://my.telegram.org)
- [Seers Markets](https://seers.market)
- [Seers Markets Website](https://www.seersmarket.com)
- [ClawHub Skill Release](https://clawhub.ai/youziyouzishu/skills/tg-cs-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with inline shell commands, environment configuration, and Python code files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and operating guidance for a Telegram userbot that uses local markdown knowledge base files, an Anthropic-compatible model API, and human handoff routing.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
