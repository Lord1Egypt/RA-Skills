## Description:

Use when writing or fixing the HTML of an email for UniOne — welcome, password reset, OTP, receipts, notifications, newsletters — making it render in Gmail, Outlook and Apple Mail, adding substitutions and logic with the UniOne template engines (simple, Velocity, Liquid), storing it with template/set, or opening it in the UniOne visual editor for the user to edit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unione](https://clawhub.ai/user/unione)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to create or update UniOne email templates for common transactional and marketing messages, with HTML and matching plaintext content that follow email client constraints. They can choose a template engine, store a template, and prepare it for review and testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Test sends could expose sensitive values.

Mitigation: Use synthetic data for testing and do not send credentials, one-time codes, or password-reset tokens.

## Reference(s):

- [UniOne API documentation](https://docs.unione.io/en/web-api-ref)
- [Template engine reference](artifact/references/engines.md)
- [HTML email guidance](artifact/references/html-email.md)
- [ClawHub skill release](https://clawhub.ai/unione/skills/unione-email-templates)

## Skill Output:

**Output Type(s):** [Code, Configuration, Guidance]

**Output Format:** [HTML and plaintext email content, with JSON API request examples and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Email content may use simple, Liquid, Velocity, or none template syntax.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
