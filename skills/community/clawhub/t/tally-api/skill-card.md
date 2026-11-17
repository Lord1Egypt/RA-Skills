## Description:

Helps agents manage Tally forms, submissions, workspaces, webhooks, and organization membership through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams using Tally can ask an agent to review and manage forms, submissions, workspaces, webhooks, and organization access. It can also guide approved automations that act on a connected Tally account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account changes and organization membership actions can alter data or access.

Mitigation: Confirm the connected account, resource identifiers, intended changes, and affected people before each write.

Risk: Webhooks and automated triggers can continuously forward form submissions, including personal information.

Mitigation: Approve each destination URL and ongoing data flow separately; revoke unused webhooks and automations.

Risk: Long-lived API keys can expose account access if disclosed.

Mitigation: Prefer OAuth, avoid displaying or storing keys, and revoke unused connections.

## Reference(s):

- [Tally skill release](https://clawhub.ai/byungkyu/skills/tally-api)
- [Tally API introduction](https://developers.tally.so/api-reference/introduction)
- [Tally API reference](https://developers.tally.so/llms.txt)
- [Maton homepage](https://maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Scheduled trigger reference](artifact/references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Tally account data; write actions require explicit user approval.]

## Skill Version(s):

1.2.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
