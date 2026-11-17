## Description:

Books same-city on-demand courier deliveries in China via Tencent Mobility MCP and supports order status, rider tracking, cancellation, and token setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

External users in China use this skill to book and manage same-city courier pickup-and-deliver errands through an agent. It guides address collection, quote selection, payment handoff, order tracking, rider status checks, and cancellation.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill requires a Tencent delivery token and can store delivery names, phone numbers, precise addresses, and coordinates locally.

Mitigation: Use only on trusted devices, avoid shared machines, and delete token, session, and address-book data when no longer needed.

Risk: Booking, cancellation, and payment flows can create charges or modify active courier orders.

Mitigation: Confirm addresses, service option, fees, cancellation fees, and payment links in WeChat or Tencent before paying or cancelling.

Risk: The server security summary marks the release suspicious because it handles tokens, precise addresses, cancellations, and payment links.

Mitigation: Review the skill before installing and use it only if that data access and payment handling are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tencent-adm/skills/tencent-delivery-skill)
- [Delivery workflow](references/delivery-workflow.md)
- [Order workflow](references/order-workflow.md)
- [Quick start and token workflow](references/quick-start-workflow.md)
- [MCP API contract](references/api-contract.md)
- [Error handling](references/error-handling.md)
- [Session state](references/session-state.md)
- [Address book preferences](assets/PREFERENCE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline shell commands and structured JSON tool results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include WeChat payment handoff, order status text, masked contact details, and address-selection prompts; token values and internal booking identifiers should not be shown to users.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
