## Description:

Send and read messages on Facebook Messenger, WhatsApp, Instagram, LinkedIn, Twitter/X, Signal, Telegram, Discord and other networks through a Beeper account, using cloud Matrix bridges with E2EE setup, cross-signing, inbound decryption support, and Python/CLI wrappers for chat operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkobject](https://clawhub.ai/user/jkobject)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an agent to their own Beeper account so it can list, search, read, summarize, and send messages across bridged chat networks with explicit user control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable access to private chats and bridged messaging accounts can expose sensitive conversations or enable unintended sends.

Mitigation: Install only on a trusted, dedicated machine or account, protect the Beeper recovery key, access token, and local Olm store, and require explicit user approval before sending messages.

Risk: Installer and dependency choices may introduce supply-chain or local system risk.

Mitigation: Review the installer before running it, pin and verify bbctl and Python dependencies, and avoid using the legacy client.py send path.

Risk: Digest generation, plaintext key exports, or temporary files may leak private message content or credentials.

Mitigation: Do not use /tmp for private digests or plaintext key exports; store sensitive files in permission-restricted directories and remove exports after use.

Risk: The sync daemon maintains persistent background access to new private-message keys.

Mitigation: Enable the daemon only when persistent decryption is needed and the operator accepts continuous background access to private-message keys.

## Reference(s):

- [Unbridled GitHub repository](https://github.com/jkobject/unbridled)
- [Architecture](references/architecture.md)
- [Setup checklist](references/setup-checklist.md)
- [ClawHub skill page](https://clawhub.ai/jkobject/skills/unbridled)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and generated message or digest text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May operate on private chat content and may produce outbound message text that requires user approval before sending.]

## Skill Version(s):

0.2.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
