## Description:

Generates Chinese-language restaurant supply-chain cost analysis reports covering supplier comparisons, cost card analysis, category cost trends, anomaly detection, and cost reduction recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lwh111-qh](https://clawhub.ai/user/lwh111-qh)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement and operations teams use this skill to analyze restaurant supply-chain cost files, compare suppliers, decompose cost variance, flag anomalies, and prepare phased cost reduction recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation terms may trigger the skill for general procurement or supply-chain questions.

Mitigation: Confirm that the user wants restaurant supply-chain cost analysis before applying the full report workflow.

Risk: Business cost files can contain sensitive supplier, pricing, and procurement data.

Mitigation: Use only files the user is comfortable analyzing in the active agent session and avoid exposing source data beyond the requested report.

Risk: Cost findings and recommendations can be misleading when source data is incomplete or inconsistent.

Mitigation: Call out missing fields, unit inconsistencies, time periods, and anomaly thresholds instead of filling gaps with unsupported assumptions.

## Reference(s):

- [Domain rules reference](artifact/references/domain-rules.md)
- [ClawHub skill page](https://clawhub.ai/lwh111-qh/skills/supply-chain-cost-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Chinese-language Markdown report with tables, findings, anomaly alerts, and cost reduction recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses RMB units and should label time periods when source data supports comparisons.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
