## Description:

Relay for Telegram lets agents search, retrieve, summarize, and extract structured information from a user's synced Telegram message history through Relay's read-only API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[relayintel](https://clawhub.ai/user/relayintel)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to answer questions about synced Telegram conversations, search message history, summarize chats, and extract action items or decisions from private communication data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose private synced Telegram message history to an agent and a third-party Relay service.

Mitigation: Install only when the user trusts Relay with Telegram data, keep RELAY_API_KEY in managed secrets or environment variables, and limit responses to necessary excerpts with summaries for the rest.

Risk: Automatic model invocation can cause Telegram message access without a separate explicit command for each request.

Mitigation: Require explicit invocation for sensitive deployments by setting disable-model-invocation to true or by removing RELAY_API_KEY when message access is not needed.

Risk: Telegram authentication codes, 2FA passwords, API keys, and OAuth tokens are sensitive credentials.

Mitigation: Do not put real verification codes or 2FA passwords into chat transcripts, shell history, logs, or config files; use secure secret storage for tokens and API keys.

Risk: Billing, upgrade, and referral endpoints can trigger account or payment-related workflows outside the core read-only message-search use case.

Mitigation: Treat billing, upgrade, checkout, portal, cancellation, and referral actions as requiring separate explicit user approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/relayintel/skills/relay-for-telegram)
- [Relay homepage](https://relayfortelegram.com)
- [Relay API base](https://relayfortelegram.com/api/v1)
- [Relay skill documentation](https://relayfortelegram.com/skill.md)
- [Relay agent documentation](https://relayfortelegram.com/agents.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance, API calls]

**Output Format:** [Markdown with inline shell commands and optional JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RELAY_API_KEY and returns information derived from previously synced Telegram messages.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
