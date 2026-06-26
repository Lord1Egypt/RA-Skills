## Description: <br>
Book real-world services through Lokuli MCP. Use when user needs to find, check availability, or book local services like plumbers, electricians, cleaners, mechanics, barbers, personal trainers, etc. Triggers on requests like "book me a haircut", "find a plumber near me", "I need a smog check", "schedule a massage", or any local service request. 75+ service categories available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to find local service providers, compare pricing and availability, and create a booking after explicit confirmation. It supports common service categories such as auto, beauty, wellness, home, education, tech repair, photography, and events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate booking and payment flows for real-world services. <br>
Mitigation: Confirm the provider, service, price, date, and time with the user before creating a booking or sharing a payment link. <br>
Risk: Booking requires sharing customer contact details with the booking service and provider. <br>
Mitigation: Collect only the required name, email, and phone number, and remind the user to share only details they are comfortable sending. <br>
Risk: The skill depends on a third-party service for local-service search, availability, bookings, and payment links. <br>
Mitigation: Install and use the skill only when the user trusts Lokuli for local-service booking. <br>


## Reference(s): <br>
- [Service Booking on ClawHub](https://clawhub.ai/edwardrodriguez703-design/service-booking) <br>
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown and JSON-RPC tool call arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return provider options, availability, pricing, booking status, or a Stripe checkout URL after user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
