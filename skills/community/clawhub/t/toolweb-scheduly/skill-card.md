## Description:

A scheduling and booking management platform with Google Calendar integration, event type management, availability rules, and time slot booking capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to work with Scheduly scheduling workflows, including event type setup, availability rules, public booking pages, booking lifecycle management, blocked dates, and Google Calendar connection actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports sensitive booking, calendar, availability, renewal, and scheduler operations without documented authentication, authorization, or confirmation controls.

Mitigation: Review provider documentation and enforce authentication, ownership checks, and explicit confirmation before granting access to production scheduling data or destructive and paid actions.

Risk: The security evidence specifically calls out guest names, emails, notes, Google connection state, and coin renewals as sensitive.

Mitigation: Limit data exposure, avoid unnecessary collection in prompts and logs, and treat calendar connection and renewal operations as sensitive account actions.

Risk: The scheduler endpoint processes expirations, auto-renewals, and notifications.

Mitigation: Restrict scheduler access to trusted internal automation and require operational review before enabling automated renewal processing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-scheduly)
- [Scheduly API Base Route](https://api.toolweb.in/tools/scheduly)
- [Scheduly API Docs](https://api.toolweb.in:8160/docs)
- [ToolWeb](https://toolweb.in)
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/)
- [RapidAPI Publisher Profile](https://rapidapi.com/user/mkrishna477)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Configuration instructions, Guidance]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May handle scheduling data including guest names, emails, notes, calendar connection state, booking times, availability rules, blocked dates, and renewal actions.]

## Skill Version(s):

1.0.0 (source: evidence release, target metadata, and OpenAPI info)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
