## Description:

R&D Initiation Review Zhcn helps agents produce Chinese-language R&D project initiation and proposal reviews for go/no-go decisions, public novelty boundary checks, innovation-point assessment, and evidence-backed project ratings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external reviewers, and developers use this skill to review concrete R&D proposals or project packages in Chinese. It separates proposal claims from external evidence before producing go/no-go recommendations, novelty notes, risk findings, and evidence ledgers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive proposal material may be exposed if an agent sends user-provided documents to external patent, paper, or web-search tools.

Mitigation: Review proposal contents and restrict or redact confidential material before permitting external searches.

Risk: Proposal claims can be mistaken for verified facts during review.

Mitigation: Keep proposal statements, external evidence, reasoned inferences, and open gaps separate in the report and claim ledger.

Risk: Public searches may not prove internal duplicate-project coverage.

Mitigation: State any missing internal archive access and avoid presenting public novelty checks as complete internal duplication clearance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/rd-initiation-review-zhcn)
- [Workflow reference](artifact/references/workflow.md)
- [Source routing reference](artifact/references/source-routing.md)
- [Quality gates reference](artifact/references/quality-gates.md)
- [Evidence schema reference](artifact/references/evidence-schema.md)
- [Deliverables reference](artifact/references/deliverables.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Structured Markdown reports with CSV evidence ledgers and optional docx/pdf exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local review files such as report.md, novelty-note.md, query_log.csv, source_index.csv, and claim_ledger.csv.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
