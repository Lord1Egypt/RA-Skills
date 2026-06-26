## Description: <br>
Full-featured AI property management - addresses, cleanings, reservations, tasks, pros, and natural language messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mchusma](https://clawhub.ai/user/mchusma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External property managers, vacation-rental operators, and developers use this skill to manage TIDY property records, cleaning bookings, guest reservations, maintenance tasks, service professionals, and natural-language TIDY requests through CLI, REST API, or MCP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents using this skill can manage real property records, reservations, cleaning bookings, tasks, and service professionals. <br>
Mitigation: Require explicit human confirmation before delete, cancellation, reschedule, booking, paid-service, or other irreversible actions. <br>
Risk: The TIDY token is a long-lived credential and should be treated like a password. <br>
Mitigation: Store tokens in secure secret storage where possible, avoid shared machines and command history exposure, and revoke or log out when access is no longer needed. <br>
Risk: The security verdict is suspicious because the integration grants broad authority over live TIDY records with limited safety guidance. <br>
Mitigation: Install only when the operator is comfortable granting a TIDY-connected agent that level of authority, and review all high-impact actions before execution. <br>


## Reference(s): <br>
- [TIDY Homepage](https://tidy.com) <br>
- [TIDY Interactive API Docs](https://public-api.tidy.com/docs) <br>
- [TIDY MCP Endpoint](https://public-api.tidy.com/mcp) <br>
- [Authentication](references/authentication.md) <br>
- [MCP Server Reference](references/mcp-server-reference.md) <br>
- [REST API Reference](references/rest-api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell, JSON, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TIDY_API_TOKEN or TIDY CLI credentials to operate on live TIDY records.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
