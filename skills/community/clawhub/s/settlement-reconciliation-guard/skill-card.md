## Description:

Build a settlement reconciliation brief for marketplace, PSP, and bank payout workflows. Use when a team needs to separate true cash discrepancies from timing effects, fee issues, refund timing, reserve leakage, or order-to-payout mapping gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations teams use this skill to turn short settlement, payout, refund, fee, reserve, tax, or order-mapping prompts into concise reconciliation-control briefs for routine checks, month-end close support, escalations, and new channel setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat a heuristic reconciliation brief as accounting approval or final provider guidance.

Mitigation: Require human review before journal entries, dispute escalation, reserve handling, or provider decisions.

Risk: The brief may be incomplete when the prompt omits evidence such as payout reports, bank statements, refund logs, fee schedules, or reserve records.

Mitigation: Validate conclusions against the actual finance evidence before acting on discrepancies.

Risk: The skill does not query live financial systems and can miss current cash, settlement, or provider state.

Mitigation: Confirm material findings in settlement portals, PSP dashboards, bank feeds, or ERP records before escalation or close approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/settlement-reconciliation-guard)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Heuristic brief generated from user-supplied context; no live settlement, bank, PSP, or ERP systems are queried.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
