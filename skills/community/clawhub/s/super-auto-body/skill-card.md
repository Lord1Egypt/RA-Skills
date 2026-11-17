## Description:

Super Auto Body helps agents search for auto-body providers, check availability, and create booking requests through Lokuli MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find auto-body repair services, check appointment availability, and prepare booking requests for services such as dents or painting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal contact and booking details may be sent to an external Lokuli MCP service.

Mitigation: Use only when the user intends to search or book auto-body services, and confirm the provider, time, name, email, and phone number before sending a booking request.

Risk: The skill can create bookings without clearly requiring user confirmation.

Mitigation: Require explicit user confirmation before invoking create_booking or sending customer contact details.

## Reference(s):

- [Super Auto Body ClawHub page](https://clawhub.ai/subaru0573/skills/super-auto-body)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, JSON, API Calls]

**Output Format:** [Markdown guidance with JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide calls to search, check_availability, and create_booking tools on an external Lokuli MCP service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
