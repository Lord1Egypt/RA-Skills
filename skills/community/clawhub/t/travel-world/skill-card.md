## Description:

Search flights, hotels, rental cars, travel insurance, and experiences, and plan trips through Travel World's hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prosy](https://clawhub.ai/user/prosy)

### License/Terms of Use:

Proprietary - Augmented Worlds Inc.

## Use Case:

External users and developers use this skill to connect an MCP-capable agent to Travel World for travel search, comparison, flight-status checks, destination planning, promotions, and brand-direct travel options. Booking and payment completion are handed off to Travel World.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel searches and trip details are sent to Travel World's hosted MCP service.

Mitigation: Install the skill only when that data sharing is acceptable, and avoid sending unnecessary sensitive travel details.

Risk: The hosted MCP service can advertise new or changed tools over time.

Mitigation: Use runtime controls that review newly advertised MCP tools before execution.

Risk: Travel booking and payment steps may have financial impact.

Mitigation: Keep booking and payment completion user-confirmed on the Travel World site.

## Reference(s):

- [Travel World Homepage](https://travel.augworlds.ai)
- [Travel World MCP Server](https://travel.augworlds.ai/mcp)
- [Travel World MCP Token](https://travel.augworlds.ai/mcp-token)
- [ClawHub Skill Page](https://clawhub.ai/prosy/skills/travel-world)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown and MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Travel World API key and an MCP-capable runtime.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
