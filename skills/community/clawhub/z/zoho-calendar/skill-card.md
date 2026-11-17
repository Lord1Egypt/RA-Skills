## Description:

Helps an agent manage Zoho calendars and events through a Maton-connected account, including optional scheduled or event-triggered automations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to list, create, update, and delete Zoho Calendar events and calendars, schedule meetings, and, with approval, set up related automations through Maton.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar changes or deletion may affect events and schedules in the connected account.

Mitigation: Begin with read-only actions and confirm the account, target, and each write or deletion with the user.

Risk: Approved hosted functions or triggers can keep running after the immediate task.

Mitigation: Confirm automation creation with the user and review its trigger, destination, and ongoing behavior before enabling it.

Risk: Trigger destinations or exposed credentials could disclose account data.

Mitigation: Keep destinations on Maton-controlled hosts unless the user explicitly trusts another host, and never expose Maton API keys or OAuth credentials.

## Reference(s):

- [ClawHub Zoho Calendar skill release](https://clawhub.ai/byungkyu/skills/zoho-calendar)
- [Maton homepage](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Zoho Calendar API introduction](https://www.zoho.com/calendar/help/api/introduction.html)
- [Zoho Calendar events API](https://www.zoho.com/calendar/help/api/events-api.html)
- [Zoho Calendar calendars API](https://www.zoho.com/calendar/help/api/calendars-api.html)
- [Scheduled trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command, JSON, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include calendar API results and instructions for approved automations.]

## Skill Version(s):

1.2.5 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
