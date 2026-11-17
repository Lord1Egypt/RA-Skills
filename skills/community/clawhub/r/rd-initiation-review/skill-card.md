## Description:

R&D Initiation Review supports project initiation pre-screening and proposal audits for go/no-go decisions, public novelty boundary review, innovation-point assessment, and evidence-backed project rating.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External reviewers, R&D managers, innovation teams, and agent operators use this skill to review concrete project proposals, test public novelty and overlap boundaries, assess evidence sufficiency, and produce a traceable recommendation for the next decision gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential or unpublished proposal details may be sent to external search providers or recorded in local evidence files.

Mitigation: Require explicit approval before external retrieval, sanitize proposal-derived search terms, restrict approved providers, and protect or delete query logs after use.

Risk: A public-only or downgraded evidence path may be mistaken for exhaustive internal duplicate-project or novelty clearance.

Mitigation: State the tool tier, coverage limits, and any unavailable internal archives in method_decisions.md and in the final review.

Risk: Proposal claims may be treated as verified conclusions.

Mitigation: Maintain separate evidence labels for proposal-stated claims, externally corroborated facts, evidence-backed inferences, and open gaps.

## Reference(s):

- [Workflow](references/workflow.md)
- [Source Routing](references/source-routing.md)
- [Deliverables](references/deliverables.md)
- [Quality Gates](references/quality-gates.md)
- [Evidence Schema](references/evidence-schema.md)
- [Method Benchmark](references/method-benchmark.md)
- [ClawHub Skill Page](https://clawhub.ai/yuanzhian-patsnap/skills/rd-initiation-review)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown review package with CSV evidence logs and optional docx/pdf exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces report.md, novelty-note.md, request.md, workplan.md, method_decisions.md, query_log.csv, source_index.csv, and claim_ledger.csv in a writable run folder.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
