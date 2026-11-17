## Description:

Helps agents send transactional email and manage Resend domains, contacts, templates, broadcasts, and webhooks through a user-authorized connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to manage transactional email, mailing lists, templates, and broadcasts in their Resend account, with approval before changes or sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorizing a connection may expose email and contact data or allow access to the wrong Resend account.

Mitigation: Review the target connection and requested scopes, prefer OAuth over long-lived API keys, and authorize only the account needed.

Risk: Sending mail, deleting data, or creating API keys can cause unintended external or irreversible changes.

Mitigation: Require explicit user confirmation of the specific action before executing it.

Risk: Deployed functions and webhooks or triggers can continue processing or forwarding data after setup.

Mitigation: Review the destination and behavior, and obtain explicit confirmation before deployment or enabling ongoing automation.

## Reference(s):

- [Resend skill on ClawHub](https://clawhub.ai/byungkyu/skills/resend-api)
- [Maton](https://maton.ai)
- [Resend API documentation](https://resend.com/docs/api-reference/introduction)
- [Maton documentation](https://docs.maton.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with example commands and API request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide approved email and contact operations through a connected Resend account.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
