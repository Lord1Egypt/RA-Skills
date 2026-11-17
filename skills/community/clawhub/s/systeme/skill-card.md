## Description:

Helps agents manage Systeme.io contacts, tags, courses, communities, and subscriptions through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People managing a Systeme.io account can use this skill to look up and update contacts, tags, course enrolments, community memberships, and subscriptions. It also describes optional user-approved automations using functions and triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account writes and deletes can change or remove business data.

Mitigation: Start with read-only calls, grant the narrowest available access, and confirm every write or delete with the user.

Risk: Webhooks, triggers, functions, and executable watches can keep acting after the initial request.

Mitigation: Create them only for a named, user-approved destination and remove them when no longer needed.

## Reference(s):

- [ClawHub Systeme.io skill](https://clawhub.ai/byungkyu/skills/systeme)
- [Maton homepage](https://maton.ai)
- [Systeme.io API Reference](https://developer.systeme.io/reference)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline shell and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses may contain account data; disclose only what the task needs.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
