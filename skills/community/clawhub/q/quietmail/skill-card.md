## Description:

Provides AI agents with no-verification email accounts and a REST API for creating agent mailboxes, sending email, and listing sent or received messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[co1onnese](https://clawhub.ai/user/co1onnese)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI-agent operators use quiet-mail to provision agent-specific email identities and send, receive, or audit messages through a REST API backed by mailcow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged for review because it ships live-looking SMTP credentials and weak secret-storage defaults.

Mitigation: Remove and rotate embedded SMTP credentials, replace default database credentials, and store API keys and mailbox passwords with hashing or encryption before deployment.

Risk: Unauthenticated agent creation and advertised unlimited sending can enable account and email abuse.

Mitigation: Add real signup controls, sending quotas, rate limits, and operational abuse monitoring before exposing the service publicly.

Risk: The bundled database defaults can expose sensitive API keys and mailbox credentials if deployed unchanged.

Mitigation: Avoid public PostgreSQL exposure, restrict network access, and require deployment-specific database passwords.

Risk: The security guidance calls out vulnerable dependencies as requiring review.

Mitigation: Upgrade vulnerable dependencies and rerun security scanning before installation or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/co1onnese/skills/quietmail)
- [quiet-mail homepage](https://quiet-mail.com)
- [quiet-mail API service](https://api.quiet-mail.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples, curl commands, and Python or Node.js snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents through API requests that create mailboxes, send email, and list sent or received messages.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json, and application configuration)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
