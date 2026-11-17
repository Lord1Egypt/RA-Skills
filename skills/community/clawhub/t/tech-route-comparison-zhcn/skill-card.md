## Description:

基于证据的两条或多条技术路线、架构或解决方案路径的对比分析，用于技术预研、技术路线对比、路线选型、TRL 或成熟度评估、机会图谱，以及面向管理层的技术报告交付物。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and technical decision makers use this Chinese-language skill to compare technical routes, assess maturity or TRL, normalize comparison criteria, and produce evidence-backed recommendations for research, feasibility, or leadership review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential R&D, patent, or strategy topics may expose sensitive query details when the workflow falls back to public search providers.

Mitigation: Confirm approved search providers before use and redact sensitive query terms or proprietary details during public-search fallback.

Risk: Technical route recommendations can mislead decision makers if the route set, comparison basis, evidence coverage, or counter-evidence checks are incomplete.

Mitigation: Use the bundled comparison basis, source index, claim ledger, and quality gates before treating a report as decision-ready.

## Reference(s):

- [Workflow](references/workflow.md)
- [Deliverables](references/deliverables.md)
- [Source Routing](references/source-routing.md)
- [Evidence Schema](references/evidence-schema.md)
- [Quality Gates](references/quality-gates.md)
- [Method Benchmark](references/method-benchmark.md)
- [Domain Playbooks](references/domain-playbooks.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-language Markdown reports with CSV evidence logs and optional DOCX/PDF exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured local evidence files such as comparison_basis.md, query_log.csv, source_index.csv, claim_ledger.csv, and report.md.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
