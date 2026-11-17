## Description:

Todozi provides an async API client and LangChain tools for managing Eisenhower matrices, tasks, goals, notes, bulk operations, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bgengs](https://clawhub.ai/user/bgengs)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to connect Todozi task-management workflows to an async Python SDK or LangChain tools. It supports creating, listing, searching, updating, completing, and deleting matrices, tasks, goals, notes, webhooks, and user preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials and task data can be sent to a configurable Todozi endpoint.

Mitigation: Use only a Todozi API key approved for this integration, leave TODOZI_BASE at the trusted default unless the alternate endpoint is verified, and avoid entering sensitive task content unless it is appropriate for the configured service.

Risk: Delete, bulk, webhook, and preference operations can modify or remove user data or change outbound event delivery.

Mitigation: Require explicit user confirmation before executing destructive, bulk, webhook, preference, or learned_context operations, and show the target IDs or webhook URL before the call.

## Reference(s):

- [Todozi API Reference](artifact/references/api_reference.md)
- [Todozi API](https://todozi.com/api)
- [ClawHub Skill Page](https://clawhub.ai/bgengs/skills/todozi)
- [ClawHub Publisher Profile](https://clawhub.ai/user/bgengs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell examples plus LangChain tool string responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Todozi API key and may call the configured Todozi API endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
