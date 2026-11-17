## Description:

Helps agents read, send, search, and organize Zoho Mail through a Maton-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams with a connected Zoho Mail account use this skill to retrieve messages, send replies, and manage folders and labels. It also guides setup of separately approved hosted functions and event or scheduled triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting the wrong account or granting more access than needed exposes mail data.

Mitigation: Confirm the intended account before authorization, select only needed permissions, and specify the connection for each operation.

Risk: Sending, changing, or deleting mail may disclose information or cause irreversible changes.

Mitigation: Review recipients, account, affected messages, and intended changes; obtain explicit approval before each write.

Risk: Hosted functions, triggers, or destinations can continue acting or forwarding data after setup.

Mitigation: Review their code, schedule or event source, and destination before approval; remove automation when no longer needed.

Risk: API credentials and returned messages may expose private information.

Mitigation: Use managed sign-in when available, do not print or store credentials, and limit displayed mail content to the requested information.

## Reference(s):

- [Zoho Mail skill release](https://clawhub.ai/byungkyu/skills/zoho-mail)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Zoho Mail API overview](https://www.zoho.com/mail/help/api/overview.html)
- [Scheduled trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown guidance with CLI examples and selected API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may contain personal email data; share only fields needed for the task.]

## Skill Version(s):

1.2.5 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
