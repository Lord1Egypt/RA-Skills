## Description:

Read, send, and manage Gmail emails, threads, labels, and drafts via Gmail API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent work with a configured Gmail account, including reading messages, searching mail, sending email, managing labels, and working with drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose private mailbox data and exercise real email-sending or mailbox-modification authority for the configured Gmail account.

Mitigation: Install only for intended accounts, store OAuth credentials securely, grant the narrowest Gmail scopes that fit the use case, and review recipients, attachments, drafts, and label changes before send or modify operations.

## Reference(s):

- [Gmail API documentation](https://developers.google.com/gmail/api)
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/tc-gmail)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with JSON examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Gmail OAuth environment variables and Google API Python packages.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
