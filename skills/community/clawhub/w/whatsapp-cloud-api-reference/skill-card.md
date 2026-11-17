## Description:

Use when implementing WhatsApp messaging via Meta Cloud API, or diagnosing failures like message not delivered, template rejected, webhook issues, phone not registered, token errors, rate limiting, 24-hour window violations, quality rating drops, or setup mistakes on the WhatsApp Business API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romanbaz](https://clawhub.ai/user/romanbaz)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill as a practical reference for setting up Meta WhatsApp Cloud API messaging, sending template and media messages, configuring webhooks, and troubleshooting common delivery, token, rate-limit, and account-health failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reference may encourage use of overpowered or long-lived WhatsApp API credentials.

Mitigation: Use scoped non-admin credentials where possible, store secrets outside prompts and shell history, rotate tokens, and review credential permissions before production use.

Risk: Copy-paste examples may expose real phone numbers, message bodies, or tokens in logs, URLs, or command history.

Mitigation: Redact message contents and recipient identifiers from logs, avoid placing tokens in URLs or copied shell commands, and use a secrets manager for local and deployed environments.

Risk: Recipient validation or test sends can accidentally message real users or contact people without consent.

Mitigation: Validate recipients through a non-messaging path where possible, require documented opt-in before sending, and test against approved sandbox or consenting numbers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romanbaz/skills/whatsapp-cloud-api-reference)
- [Publisher profile](https://clawhub.ai/user/romanbaz)
- [Meta Graph API versions endpoint](https://graph.facebook.com/versions)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup checklists, API payload examples, webhook patterns, troubleshooting tables, and operational constraints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
