## Description:

Helps agents read and manage Zoho Bigin CRM records through a connected Maton account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams and their agents use this skill to find and manage contacts, companies, pipelines, and products in a connected Zoho Bigin account. It also guides approved CRM actions and optional automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CRM writes or account connections can change or expose business data.

Mitigation: Start with read-only requests and obtain explicit user approval before connections or writes; use only required OAuth scopes.

Risk: Authentication credentials or CRM responses may expose sensitive information.

Mitigation: Prefer OAuth, do not reveal or store credentials, and limit displayed record fields to what the task requires.

Risk: Persistent triggers or third-party destinations may keep forwarding event data.

Mitigation: Require explicit approval for automations and external destinations; review and remove triggers when no longer needed.

## Reference(s):

- [Zoho Bigin skill on ClawHub](https://clawhub.ai/byungkyu/skills/zoho-bigin)
- [Zoho Bigin API overview](https://www.bigin.com/developer/docs/apis/v2/)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown with CRM record summaries and command or code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include personal CRM data; show only fields needed for the task.]

## Skill Version(s):

1.2.6 (source: server-resolved ClawHub release; skill frontmatter lists 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
