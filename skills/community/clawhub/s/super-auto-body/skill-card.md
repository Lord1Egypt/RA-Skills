## Description: <br>
Super Auto Body helps agents search for auto-body repair providers, check appointment availability, and create bookings through Lokuli MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and service agents use this skill to find nearby auto-body repair, dent, and painting services, compare availability, and prepare bookings through Lokuli MCP. Because bookings may send personal contact details, agents should show the provider, service, time, and exact personal details before creating an appointment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may create a third-party booking without clear user consent. <br>
Mitigation: Require explicit confirmation before booking and show the provider, service, appointment time, and all customer details first. <br>
Risk: Booking requests may send personal contact information to Lokuli. <br>
Mitigation: Use the skill only when sharing booking details and personal contact information with Lokuli is acceptable to the user. <br>


## Reference(s): <br>
- [Super Auto Body on ClawHub](https://clawhub.ai/subaru0573/skills/super-auto-body) <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls] <br>
**Output Format:** [Markdown with JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SSE and JSON-RPC 2.0 examples for search, availability checks, and booking creation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
