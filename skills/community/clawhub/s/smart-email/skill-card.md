## Description:

Email assistant skill — check emails, AI summaries, daily digests. Supports Gmail, Outlook/M365, Google Workspace. Users interact through their chat platform (Telegram, Feishu, WhatsApp, etc.).

This skill is ready for commercial/non-commercial use.

## Publisher:

[jundonggit](https://clawhub.ai/user/jundonggit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to check configured mailboxes, read messages, and generate AI-assisted summaries or daily email digests from chat-based workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read private email and store reusable mailbox or OAuth credentials.

Mitigation: Use only in a trusted local environment, prefer OAuth over app passwords, and review credential storage controls before installing.

Risk: Email contents can be sent to an external AI provider for summaries and digests.

Mitigation: Configure only an approved AI provider and avoid summarizing sensitive mail unless that data flow is allowed.

Risk: Custom IMAP server support has unsafe TLS validation according to the security guidance.

Mitigation: Avoid custom IMAP servers until TLS validation is fixed.

Risk: The optional web admin UI exposes mailbox configuration and actions through a local server protected by a token.

Mitigation: Run the web UI only on trusted machines and keep the token-bearing URL private.

## Reference(s):

- [ClawHub Smart Email Skill Page](https://clawhub.ai/jundonggit/skills/smart-email)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jundonggit)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON command responses and concise chat-ready text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI commands return structured JSON; summaries and digests are generated from mailbox content when an AI API key is configured.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
