## Description:

Send transactional and marketing emails via UniOne Email API, manage email templates, validate email addresses, check delivery statistics, manage suppression lists, configure webhooks, and handle domain settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[selzy-openclaw](https://clawhub.ai/user/selzy-openclaw)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and external users can use this skill to let an agent prepare UniOne Email API requests for sending email, validating addresses, configuring delivery tracking, checking domains, and managing related account resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to operate a UniOne account using an API key.

Mitigation: Use a least-privilege UniOne API key, prefer UNIONE_API_KEY or a secret manager, and do not paste real keys into chat.

Risk: Email sending can contact real recipients and create account activity.

Mitigation: Require explicit confirmation before sending email and review the recipient, subject, and body summary before execution.

Risk: Template, webhook, suppression, tag, event dump, and project operations can change or delete account resources.

Mitigation: Require confirmation before account-changing operations and review the exact target resource before proceeding.

Risk: Retries on email sends can create duplicate messages if the request is not idempotent.

Mitigation: Use an idempotency key for each logical send operation and reuse that key only when retrying the same send.

## Reference(s):

- [UniOne API Documentation](https://docs.unione.io/en/web-api-ref)
- [UniOne Getting Started Guide](https://docs.unione.io/en/)
- [UniOne Template Engines](https://docs.unione.io/en/web-api#section-template-engines)
- [UniOne Website](https://unione.io/en/)
- [ClawHub Skill Page](https://clawhub.ai/selzy-openclaw/skills/unione)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON, curl, and language-specific code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces API request guidance for UniOne operations that require a UniOne account, a verified sending domain, and UNIONE_API_KEY.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
