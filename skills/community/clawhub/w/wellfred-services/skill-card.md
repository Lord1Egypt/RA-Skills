## Description:

Find services and providers in Costa Rica, submit customer-approved quote requests, and prepare email-verified booking requests through WellFred's public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leesalminen](https://clawhub.ai/user/leesalminen)

### License/Terms of Use:

MIT-0

## Use Case:

Customers and agents find and compare Costa Rica services, request quotes with customer approval, and prepare booking requests that customers confirm through WellFred email verification.

### Deployment Geography for Use:

Costa Rica (offerings; customers may be abroad)

## Known Risks and Mitigations:

Risk: Quote or booking requests can disclose customer contact, location, timing, and service details to WellFred.

Mitigation: Summarize the request and obtain the customer's approval before submitting it.

Risk: A prepared booking request may be mistaken for a confirmed reservation.

Mitigation: Explain that the customer must verify and confirm by email through WellFred; report any pending provider acceptance without claiming a booking.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/leesalminen/skills/wellfred-services)
- [WellFred public agent guide](https://app.wellfred.com/agents.md)
- [WellFred OpenAPI contract](https://app.wellfred.com/openapi.json)
- [WellFred authentication guide](https://app.wellfred.com/auth.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text with offering links and request references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes returned prices and pricing units where available; booking intents require customer email verification and do not hold a slot.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
