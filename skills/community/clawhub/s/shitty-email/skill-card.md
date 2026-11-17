## Description:

Create and manage temporary disposable email inboxes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johanski](https://clawhub.ai/user/johanski)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to create disposable inbound email addresses, check temporary inboxes, retrieve email content, extract verification codes or links, extend inbox lifetime, and delete inboxes after use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Temporary inbox tokens grant access to the disposable inbox while they are valid.

Mitigation: Treat inbox tokens like short-lived credentials and avoid sharing them.

Risk: Disposable addresses can be misused on services where temporary email violates rules or bypasses anti-abuse controls.

Mitigation: Use disposable addresses only where authorized and consistent with the target site's terms and anti-abuse expectations.

Risk: The skill depends on an external temporary email service and sends inbox operations to that service.

Mitigation: Install only if use of the shitty.email service is acceptable for the intended workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/johanski/skills/shitty-email)
- [Shitty Email Service](https://shitty.email)
- [Shitty Email Inbox API](https://shitty.email/api/inbox)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; uses temporary inbox tokens for subsequent inbox, email retrieval, extension, and deletion operations.]

## Skill Version(s):

1.0.2 (source: server release metadata, created 2026-02-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
