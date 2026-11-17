## Description:

Design and review user and operations messaging, flows, and support templates for UPI payments, mandates, refunds, disputes, and incident communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anugotta](https://clawhub.ai/user/anugotta)

### License/Terms of Use:

MIT-0

## Use Case:

Product, design, customer experience, and operations teams use this skill to create clear UPI payment state copy, mandate consent messaging, support macros, escalation playbooks, refund and dispute communication, and incident messaging.

### Deployment Geography for Use:

India

## Known Risks and Mitigations:

Risk: UPI payment regulations, PSP behavior, mandate expectations, refund timelines, and escalation requirements can change after the skill's last verification date.

Mitigation: Verify current RBI, NPCI, PSP, and internal legal/compliance expectations before using generated copy or workflows in production.

Risk: Generic SLA windows or status wording could mislead users if they do not match the organization's provider status taxonomy or reconciliation process.

Mitigation: Adapt SLA windows, pending/failure semantics, reference ID fields, and escalation ownership to the payment provider and support operations process.

Risk: Guidance output could be mistaken for payment execution, legal advice, or compliance approval.

Mitigation: Use the skill only for messaging and operations drafts, then validate in sandbox or staging and route through approved policy, legal, compliance, and support review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anugotta/skills/upi-payment-ux-ops)
- [RBI authentication direction](https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12898)
- [RBI recurring e-mandate update](https://www.rbi.org.in/scripts/FS_Notification.aspx?Id=12570&Mode=0&fn=9)
- [Example provider webhook behavior](https://razorpay.com/docs/webhooks/payments/?preferred-country=IN)
- [Setup checklist](setup.md)
- [UPI UX and ops reference](reference.md)
- [Examples](examples.md)
- [UX/Ops validation checklist](validation-checklist.md)
- [Launch playbook](launch-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured copy blocks, support macros, escalation matrices, and validation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance-only output; does not execute payments, move funds, or provide production legal/compliance approval.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
