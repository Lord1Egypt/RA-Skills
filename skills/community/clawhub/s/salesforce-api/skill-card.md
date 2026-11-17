## Description:

Helps an agent query and manage Salesforce CRM records through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Salesforce administrators and developers use this skill to inspect CRM records, make approved changes, and configure related automations through their authorized connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CRM writes or batch actions may change or delete unintended records.

Mitigation: Confirm the connection, affected record IDs, and intended effects before writes; test destructive or batch work in a sandbox org.

Risk: Broad Salesforce permissions or unused connections may leave access beyond the task.

Mitigation: Use the narrowest available Salesforce scopes and remove unused connections promptly.

Risk: Leftover functions, triggers, or destinations may continue to run after the task.

Mitigation: Remove functions, triggers, and destinations when they are no longer needed.

## Reference(s):

- [Salesforce skill on ClawHub](https://clawhub.ai/byungkyu/skills/salesforce-api)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Salesforce REST API Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_rest.htm)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, a Maton account, and an authorized Salesforce connection.]

## Skill Version(s):

1.2.8 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
