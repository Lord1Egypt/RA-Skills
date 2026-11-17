## Description:

Book real-world services through Lokuli MCP for finding, checking availability, and booking local service providers across categories such as home, auto, beauty, wellness, education, photography, and events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search for local service providers, compare pricing and availability, create confirmed bookings, and receive payment checkout links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The booking workflow can send location, appointment, contact, and selected service details to Lokuli and can direct the user into a Stripe checkout flow.

Mitigation: Only proceed after the user confirms the provider, price, time slot, and intent to book, and collect personal details only when needed for the booking.

Risk: A booking could be created for the wrong provider, service, price, or appointment time if the user has not reviewed the details.

Mitigation: Present pricing and availability clearly, fetch provider details before booking, and require explicit user approval before calling the booking tool.

## Reference(s):

- [Service Booking ClawHub Page](https://clawhub.ai/edwardrodriguez703-design/skills/service-booking)
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse)
- [Publisher Profile](https://clawhub.ai/user/edwardrodriguez703-design)

## Skill Output:

**Output Type(s):** [guidance, API Calls, JSON, markdown]

**Output Format:** [Markdown guidance with JSON-RPC MCP tool call arguments and checkout links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider details, pricing estimates, availability slots, booking identifiers, and Stripe checkout URLs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
