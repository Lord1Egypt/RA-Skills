## Description: <br>
Manage vacation rental turnovers, guest reservations, and cleaning schedules across TIDY CLI, MCP server, and REST API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mchusma](https://clawhub.ai/user/mchusma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Airbnb hosts, VRBO managers, short-term rental operators, and property managers use this skill to have an agent plan, schedule, monitor, cancel, or reschedule vacation-rental turnovers and guest reservations through TIDY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad authority over rental operations, including booking, canceling, deleting, and rescheduling work. <br>
Mitigation: Require explicit user approval before any booking, cancellation, deletion, or rescheduling action is submitted to TIDY. <br>
Risk: Prompts may include sensitive property details such as addresses, access instructions, gate codes, or lockbox codes. <br>
Mitigation: Avoid sharing access codes unless strictly necessary, limit prompt context to the current task, and handle property access data as sensitive information. <br>
Risk: TIDY tokens and local credential files can grant access to rental operations and customer data. <br>
Mitigation: Store TIDY_API_TOKEN securely, protect the local credentials file, and rotate or revoke tokens when exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mchusma/vacation-rental-management) <br>
- [TIDY Homepage](https://tidy.com) <br>
- [Authentication](references/authentication.md) <br>
- [MCP Server Reference](references/mcp-server-reference.md) <br>
- [REST API Reference](references/rest-api-reference.md) <br>
- [Vacation Workflows](references/vacation-workflows.md) <br>
- [TIDY REST API Documentation](https://public-api.tidy.com/docs) <br>
- [TIDY MCP Endpoint](https://public-api.tidy.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with natural-language examples, bash commands, JSON configuration, and REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated TIDY workflows require TIDY_API_TOKEN or MCP login credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
