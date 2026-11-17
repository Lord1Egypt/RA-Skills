## Description:

Connects an agent to Twenty CRM to manage contacts, companies, opportunities, activities, and workflows through Maton-managed authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People using Twenty CRM can ask an agent to find and manage companies, contacts, deals, notes, tasks, and workspace information. With explicit approval, they can also connect an account and set up automations that act on CRM data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account connections and CRM writes can access or change data beyond the intended task.

Mitigation: Confirm the account and connection before granting access, use the narrowest available permissions, and obtain user approval before writes.

Risk: Broad triggers or external destinations can continuously forward sensitive event data.

Mitigation: Scope triggers to the requested source and events, minimize forwarded fields, and get explicit approval for each destination.

Risk: Exposed API keys or stored OAuth credentials can permit unauthorized access.

Mitigation: Keep credentials out of logs, shared outputs, destination headers, and automation payloads.

## Reference(s):

- [Twenty CRM skill on ClawHub](https://clawhub.ai/byungkyu/skills/twenty)
- [Maton homepage](https://maton.ai)
- [Twenty API documentation](https://docs.twenty.com/developers/extend/api)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton trigger source references](artifact/references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with commands, API examples, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may contain CRM data; share only what the task needs.]

## Skill Version(s):

1.2.8 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
