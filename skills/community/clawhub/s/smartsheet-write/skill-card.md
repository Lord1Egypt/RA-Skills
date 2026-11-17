## Description:

Helps an agent add or update Enterprise WeChat Smart Sheet records through user-provided webhooks and table schemas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roollond](https://clawhub.ai/user/roollond)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operators use this skill to record, update, and track structured business data in Enterprise WeChat Smart Sheet without manually opening the table. The skill is suited to tasks, logs, meetings, customer records, orders, bugs, requirements, approvals, inventory, and similar operational records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved webhook URLs act as reusable write credentials for Smart Sheet tables.

Mitigation: Save webhooks only with user consent, restrict access to the local config file, and delete or rotate webhooks if the file may have been exposed.

Risk: The skill can write sensitive business data to user-provided tables.

Mitigation: Use only with authorization from the table owner and avoid sensitive finance, personnel, or customer data unless the user is permitted to process it.

Risk: An incorrect webhook or stale schema can write records to the wrong table or with incorrect fields.

Mitigation: Confirm the target table, verify the webhook uses the real qyapi.weixin.qq.com Smart Sheet URL, and check the schema before the first reuse in a conversation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/roollond/skills/smartsheet-write)
- [Field Types Reference](references/field-types.md)
- [Usage Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with JSON payloads, shell commands, configuration snippets, and API response summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save user-provided webhook URLs and table schemas locally for later reuse when the user agrees.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
