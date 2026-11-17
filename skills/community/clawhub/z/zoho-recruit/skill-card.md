## Description:

Helps agents read and manage Zoho Recruit candidates, job openings, interviews, applications, and recruitment workflows through Maton-managed access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters and recruiting teams use this skill to find and manage candidates, job openings, interviews, and applications in their connected Zoho Recruit account. It also provides guidance for user-approved recruitment automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting Zoho Recruit gives Maton access to recruiting data.

Mitigation: Connect only a trusted account with the narrowest available OAuth scopes and confirm the account before making changes.

Risk: Writes and bulk deletions can alter or irreversibly remove records.

Mitigation: Default to reading records; confirm each write and approve deletions record by record.

Risk: Hosted functions and trigger destinations can continue forwarding event data.

Mitigation: Enable automation only with explicit approval after reviewing its destination, data flow, and persistence.

## Reference(s):

- [Zoho Recruit skill release](https://clawhub.ai/byungkyu/skills/zoho-recruit)
- [Maton](https://maton.ai)
- [Zoho Recruit API v2 overview](https://www.zoho.com/recruit/developer-guide/apiv2/)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may summarize Zoho Recruit records or describe user-approved changes and automations.]

## Skill Version(s):

1.2.5 (source: server-resolved ClawHub release metadata; skill frontmatter lists 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
