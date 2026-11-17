## Description:

Helps agents manage Zoho Bookings appointments, services, staff, and workspaces through a connected Maton account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Users and their agents can check availability and manage appointments, services, staff, and workspaces in a connected Zoho Bookings account. They can also set up approved functions and triggers for related automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an account or modifying bookings can grant access or change scheduling data.

Mitigation: Confirm each new connection and write separately; verify the target and intended change first.

Risk: Hosted functions, triggers, and destinations can repeatedly act on or forward account data.

Mitigation: Approve each function, trigger, and destination separately, including where events will be sent.

Risk: Raw API keys and returned booking details can expose credentials or personal data.

Mitigation: Prefer the CLI login, avoid raw API-key mode unless needed, and share only task-relevant response fields.

## Reference(s):

- [Zoho Bookings API documentation](https://www.zoho.com/bookings/help/api/v1/oauthauthentication.html)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton homepage](https://maton.ai)
- [Zoho Bookings skill release](https://clawhub.ai/byungkyu/skills/zoho-bookings)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected account's permissions and may contain appointment or contact details.]

## Skill Version(s):

1.2.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
