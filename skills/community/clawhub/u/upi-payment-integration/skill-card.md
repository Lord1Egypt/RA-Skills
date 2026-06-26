## Description: <br>
Design and implement robust UPI payment integrations for collect, intent, QR, and autopay mandate flows with webhook handling, idempotency, reconciliation, and RBI-aligned authentication and compliance guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anugotta](https://clawhub.ai/user/anugotta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to design, review, or troubleshoot UPI payment integrations, including payment state handling, webhook verification, reconciliation, recurring mandates, and production readiness checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider keys, merchant identifiers, webhook secrets, or payment event payloads may be exposed during implementation or troubleshooting. <br>
Mitigation: Use sandbox credentials first, keep secrets out of chat and source control, store them in a secret manager, and restrict, encrypt, audit, and retention-limit webhook and event storage. <br>
Risk: UPI provider behavior and RBI or NPCI requirements may change after the skill's last source verification date. <br>
Mitigation: Verify current PSP, RBI, and NPCI documentation before production changes, including webhook semantics, retry policy, transaction limits, mandate rules, and authentication requirements. <br>
Risk: Incorrect payment state handling can unlock goods or services before durable payment success is established. <br>
Mitigation: Treat payment lifecycle as asynchronous, require verified webhook or reconciliation success for final fulfillment, and test retries, duplicates, out-of-order events, and reconciliation paths. <br>


## Reference(s): <br>
- [NPCI UPI Product Overview](https://www.npci.org.in/what-we-do/upi/product-overview) <br>
- [RBI Authentication Mechanisms Directions, 2025](https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12898) <br>
- [RBI e-mandate recurring transaction update](https://www.rbi.org.in/scripts/FS_Notification.aspx?Id=12570&Mode=0&fn=9) <br>
- [Razorpay payment webhook documentation](https://razorpay.com/docs/webhooks/payments/?preferred-country=IN) <br>
- [Setup checklist](setup.md) <br>
- [UPI integration reference](reference.md) <br>
- [Examples](examples.md) <br>
- [Validation checklist](validation-checklist.md) <br>
- [Failure handling](failure-handling.md) <br>
- [Launch playbook](launch-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with checklists, implementation plans, code snippets, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include architecture plans, database changes, failure-mode checks, and test plans.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
