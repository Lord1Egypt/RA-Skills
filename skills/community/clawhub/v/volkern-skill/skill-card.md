## Description:

Automates Volkern CRM operations including lead management, appointment scheduling, task tracking, service catalog work, WhatsApp messaging, sales pipeline management, quotations, and contracts through an MCP server that requires Volkern API key authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexpertmx](https://clawhub.ai/user/dexpertmx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect AI agents to Volkern CRM workflows for managing leads, appointments, tasks, catalog items, WhatsApp conversations, deals, quotes, and contracts. It is intended for tenants with an appropriately scoped Volkern API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connector can change live customer records and send messages.

Mitigation: Install with a least-privilege Volkern API key and require human confirmation before sends, cancellations, record updates, catalog changes, or task completion.

Risk: The security summary reports a confirmed URL path handling weakness.

Mitigation: Validate and encode URL path IDs before using the connector with sensitive production data.

Risk: The security verdict is suspicious.

Mitigation: Prefer a pinned package version and review and scan the skill before deployment.

## Reference(s):

- [ClawHub Volkern MCP Server release](https://clawhub.ai/dexpertmx/skills/volkern-skill)
- [Volkern API base URL](https://volkern.app/api)
- [Artifact README](artifact/readme.md)
- [Artifact skill instructions](artifact/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON and shell command examples; MCP tool calls return JSON data from the Volkern API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a VOLKERN_API_KEY and may perform live CRM actions such as record updates, sends, cancellations, and task completion.]

## Skill Version(s):

1.1.1 (source: server release metadata, created 2026-03-18T15:14:38Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
