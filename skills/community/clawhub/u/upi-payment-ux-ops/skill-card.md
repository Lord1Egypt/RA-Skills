## Description: <br>
Design UPI payment user experience and operations playbooks: consent wording, payment status messaging, retries, support workflows, refunds, and dispute communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anugotta](https://clawhub.ai/user/anugotta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product, design, CX, support, and operations teams use this skill to draft and review UPI payment screen copy, support macros, escalation matrices, refund/dispute communication, and incident messaging before launch or major process changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated payment UX copy or operations guidance may be inconsistent with current PSP behavior, RBI/NPCI requirements, or the organization's real payment-state taxonomy. <br>
Mitigation: Review outputs against current PSP, RBI, and NPCI documentation, legal/compliance constraints, and backend payment-state sources before production use. <br>
Risk: Pending, failed, refund, or retry messaging could misstate debit certainty, duplicate-charge risk, or expected timelines. <br>
Mitigation: Validate wording and workflows in sandbox or staging, confirm provider and bank status semantics, and approve SLA windows with support and compliance owners. <br>
Risk: Support macros and escalation paths may be incomplete without organization-specific reference IDs, ownership, and incident procedures. <br>
Mitigation: Configure available UTR, provider payment ID, and order ID fields, plus L1/L2/L3 ownership and escalation channels, before using generated support materials. <br>


## Reference(s): <br>
- [First-use checklist](setup.md) <br>
- [Release operations playbook](launch-playbook.md) <br>
- [UPI UX and ops reference](reference.md) <br>
- [Reusable UX copy and support scripts](examples.md) <br>
- [Launch validation checklist](validation-checklist.md) <br>
- [RBI authentication direction](https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12898) <br>
- [RBI recurring e-mandate update](https://www.rbi.org.in/scripts/FS_Notification.aspx?Id=12570&Mode=0&fn=9) <br>
- [Example provider webhook behavior](https://razorpay.com/docs/webhooks/payments/?preferred-country=IN) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured copy, templates, matrices, and metric lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; does not execute payments, move funds, or provide legal or compliance approval.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
