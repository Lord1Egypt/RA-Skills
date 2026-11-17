## Description:

Reorients Telegram chats after session resets by reading project STATUS.md details and sending project-specific group, direct-message, or new-room welcome context through the Telegram Bot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project operators use this skill to restore scoped project context in Telegram rooms or direct messages after transcript clears, room creation, or collaborator onboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project STATUS.md content may be sent to externally supplied Telegram chats without strong destination validation.

Mitigation: Verify chat IDs independently and use an allowlist before sending context injection messages.

Risk: Sensitive project, customer, or secret data in STATUS.md may be exposed through Telegram messages.

Mitigation: Keep secrets and customer data out of STATUS.md sections used by the skill, and add preview and redaction before production use.

Risk: Unescaped HTML content from project status text may affect Telegram message rendering.

Mitigation: Escape status-derived text before inserting it into HTML parse-mode messages.

## Reference(s):

- [Session Context Injector on ClawHub](https://clawhub.ai/nissan/skills/session-context-injector)
- [Telegram Bot API sendMessage endpoint](https://api.telegram.org/bot{bot_token}/sendMessage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, API Calls, Guidance]

**Output Format:** [Markdown guidance with Python code snippets and HTML-formatted Telegram message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TELEGRAM_BOT_TOKEN; generated Telegram messages should stay within Telegram's 4096-character message limit.]

## Skill Version(s):

1.0.0 (source: frontmatter and changelog, released 2026-04-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
