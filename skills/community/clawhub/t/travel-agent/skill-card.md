## Description:

Find, book, and change flights for your human via email. One message, and done. (by BonBook)

This skill is ready for commercial/non-commercial use.

## Publisher:

[aszelem](https://clawhub.ai/user/aszelem)

### License/Terms of Use:

MIT

## Use Case:

External users and their agents use this skill to request flight searches, bookings, changes, cancellations, and check-in related travel workflows through BonBook email exchanges. It requires existing email send and receive permissions and human approval for account setup, payment entry, and travel transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses email send and receive permissions for travel workflows, which can expose mailbox access beyond BonBook messages depending on the agent platform.

Mitigation: Install only where the human is comfortable granting email access, and constrain agent behavior to BonBook booking messages when platform controls allow it.

Risk: Payment, booking-change, and cancellation flows may proceed without consistently requiring final approval of the exact transaction.

Mitigation: Require explicit human approval of itinerary, passenger, restrictions, refund terms, fees, and final total before every booking, paid change, or cancellation; keep payment entry and CVC verification human-controlled.

Risk: Travel requests and booking details are shared with BonBook to fulfill the service.

Mitigation: Use the skill only when sharing travel details with BonBook is acceptable and avoid sending sensitive PII, credentials, or card data by email.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aszelem/skills/travel-agent)
- [BonBook Website](https://bonbook.co)
- [BonBook Access](https://bonbook.co/access)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Email instructions, Configuration instructions]

**Output Format:** [Markdown guidance with email workflow steps and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit human approval for setup, payment entry, bookings, paid changes, and cancellations.]

## Skill Version(s):

2.4.1 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
