## Description:

查询、介绍和预约小安智能健身的一对一线下私教训练服务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[han815757857-cmd](https://clawhub.ai/user/han815757857-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer questions about Xiaoan Smart Fitness private training, collect booking details, create confirmed booking requests, and check booking status through the merchant MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The merchant token could be used by the bundled client to call MCP tools beyond the declared booking tools.

Mitigation: Install only if the merchant MCP server and credential scope are trusted; before production use, restrict the client and server credential to list_services, create_booking, and get_booking.

## Reference(s):

- [小安智能健身服务目录](references/service-catalog.md)
- [小安智能健身 MCP 工具契约](references/mcp-tools.md)
- [ClawHub skill page](https://clawhub.ai/han815757857-cmd/skills/xiaoan-smart-fitness)
- [ClawHub metadata homepage](https://github.com/han815757857-cmd/xiaoan-smart-fitness)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, API calls]

**Output Format:** [Conversational text with optional shell commands and JSON tool arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses merchant MCP tools for service listing, booking creation, and booking lookup when authorized.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
