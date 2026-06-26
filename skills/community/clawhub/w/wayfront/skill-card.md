## Description: <br>
Connect to a Wayfront workspace via MCP and query business data, including clients, orders, tickets, subscriptions, invoices, and related workspace records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wayfront-bot](https://clawhub.ai/user/wayfront-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators and agents with authorized access to a Wayfront workspace use this skill to inspect workspace business records, troubleshoot client activity, and answer operational questions across clients, orders, tickets, invoices, subscriptions, services, templates, team records, and audit logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve sensitive Wayfront workspace data, including client, billing, support, team, template, and audit-log information. <br>
Mitigation: Install only for agents authorized to view the connected workspace, use the least-privileged MCP token available, keep queries narrow, and avoid sharing retrieved data outside trusted channels. <br>
Risk: Available MCP tools and fields are discovered at runtime, so the accessible data surface may change as the live Wayfront MCP API changes. <br>
Mitigation: Review the live tool list and schemas before use, and confirm token permissions when tools return unauthenticated, forbidden, or validation errors. <br>


## Reference(s): <br>
- [Wayfront Homepage](https://wayfront.com) <br>
- [ClawHub Wayfront Skill](https://clawhub.ai/wayfront-bot/wayfront) <br>
- [Publisher Profile](https://clawhub.ai/user/wayfront-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with MCP tool calls and JSON-style query examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live MCP tool schema as the authoritative source for available entities, filters, sorting, pagination, and permissions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
