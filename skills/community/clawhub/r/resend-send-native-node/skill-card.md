## Description:

Resend Send Native Node sends email via Resend.com's HTTPS API using native Node.js, with dry-run defaults and gated real sends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jwestburg](https://clawhub.ai/user/jwestburg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when a user explicitly asks to send an email, message, report, or notification through Resend. It supports previewing the exact payload before delivery and requires explicit send approval plus a recipient allowlist for real sends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real email sends are externally mutating and may deliver incorrect or unapproved content.

Mitigation: Draft and dry-run first, review the exact recipients, headers, subject, and body, and use --send only after explicit user approval.

Risk: Emailing raw logs, transcripts, secrets, or private workspace context can expose sensitive information through Resend.

Mitigation: Send only curated, reviewed content that the user is comfortable transmitting externally.

Risk: A broad or agent-modified recipient allowlist can bypass the intended recipient control for real sends.

Mitigation: Keep RESEND_ALLOWED_TO narrow and operator-controlled, and do not widen it merely to make a send succeed.

Risk: Network timeouts or server-side errors can leave delivery status ambiguous and cause duplicate emails if retried blindly.

Mitigation: Check the Resend dashboard before retrying any request that may have reached Resend.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jwestburg/skills/resend-send-native-node)
- [Resend](https://resend.com)
- [Resend domains](https://resend.com/domains)
- [Resend pricing](https://resend.com/pricing)
- [Resend emails API endpoint](https://api.resend.com/emails)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or JSON receipts, with Markdown usage guidance and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run receipts include payload details, body byte count, body SHA-256 values, and allowlist status; successful sends include the Resend message ID.]

## Skill Version(s):

1.0.20 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
