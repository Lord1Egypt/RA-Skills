## Description:

Full-featured AI property management: addresses, cleanings, reservations, tasks, pros, and natural language messaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mchusma](https://clawhub.ai/user/mchusma)

### License/Terms of Use:

MIT-0

## Use Case:

Property managers, short-term rental operators, and developers use this skill to manage TIDY properties, cleaning bookings, guest reservations, maintenance tasks, service professionals, and natural-language TIDY requests through CLI, REST API, or MCP workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose broad TIDY account access, including sensitive property-management records.

Mitigation: Use only in trusted agent environments, protect TIDY_API_TOKEN like a password, and avoid placing live tokens in shell history or shared logs.

Risk: The skill can create, change, cancel, or delete bookings, properties, reservations, tasks, and related operational records.

Mitigation: Require explicit user confirmation before destructive or scheduling-changing actions, and review generated API payloads before execution.

Risk: The recommended CLI and MCP paths can execute against live TIDY accounts with long-lived credentials.

Mitigation: Prefer pinned package versions or reviewed installation paths, and revoke or rotate tokens when access is no longer needed.

## Reference(s):

- [TIDY Homepage](https://tidy.com)
- [TIDY Interactive API Docs](https://public-api.tidy.com/docs)
- [TIDY MCP Endpoint](https://public-api.tidy.com/mcp)
- [ClawHub Skill Page](https://clawhub.ai/mchusma/skills/tidy)
- [Authentication Reference](references/authentication.md)
- [MCP Server Reference](references/mcp-server-reference.md)
- [REST API Reference](references/rest-api-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON, shell, REST API, CLI, and MCP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include property-management record identifiers, API payloads, and polling steps for asynchronous TIDY messages.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
