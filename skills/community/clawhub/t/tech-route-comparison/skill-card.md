## Description:

Evidence-backed comparison of two or more technical routes, architectures, or solution paths for route selection, maturity assessment, readiness evaluation, opportunity mapping, and management-grade technical reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical analysts, and product or R&D decision-makers use this skill to compare technical routes on an explicit evidence basis, normalize comparison dimensions, assess maturity or readiness, and produce a scenario-specific recommendation with counterevidence and update triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated comparison reports and evidence logs may contain sensitive research topics, retrieved-source details, or preliminary route judgments.

Mitigation: Review report.md, source_index.csv, query_log.csv, and claim_ledger.csv before sharing or using the outputs for decisions.

Risk: If structured patent or paper retrieval is unavailable, route breadth and frontier completeness may be weaker.

Mitigation: Record the downgrade in method_decisions.md, use the best available fallback sources, and lower confidence language for breadth, novelty, and frontier claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/tech-route-comparison)
- [Workflow](references/workflow.md)
- [Deliverables](references/deliverables.md)
- [Source Routing](references/source-routing.md)
- [Quality Gates](references/quality-gates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured Markdown report plus traceable evidence files such as comparison basis, query log, source index, and claim ledger]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional docx or pdf export when the host environment supports rendering]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
