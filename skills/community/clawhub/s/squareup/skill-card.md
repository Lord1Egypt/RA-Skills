## Description:

Guides an agent to access and administer Square business data through a Maton-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Business users and developers use this skill to inspect and manage Square payments, customers, orders, and other authorized resources through Maton, with approval for changes and persistent automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected Square account can expose or change business data beyond the user's intended task.

Mitigation: Use the least-privileged account and OAuth scopes, verify the connection ID, and approve writes only after checking the endpoint, resource, and amount.

Risk: Functions, triggers, and destinations can continue acting after the immediate task ends.

Mitigation: Review persistent automation before enabling it and remove it when no longer needed.

## Reference(s):

- [Square skill release](https://clawhub.ai/byungkyu/skills/squareup)
- [Square API reference](https://developer.squareup.com/reference/square)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton homepage](https://maton.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
