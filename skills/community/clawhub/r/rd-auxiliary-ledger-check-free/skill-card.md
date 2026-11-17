## Description:

研发费用辅助账逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and R&D operations staff at high-tech enterprises use this skill to check copied R&D auxiliary ledger tables before monthly cost collection, annual high-tech reporting, or certification review. It performs local arithmetic and table-consistency checks, but does not provide tax, accounting, audit, or eligibility opinions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat deterministic ledger checks as tax, accounting, audit, or high-tech certification advice.

Mitigation: State that the skill only checks table arithmetic and consistency, and require qualified review for tax treatment, expense eligibility, audit conclusions, and certification submissions.

Risk: Users may paste unrelated sensitive documents into a tool designed for R&D auxiliary ledger tables.

Mitigation: Limit input to the required ledger table fields and avoid submitting unrelated sensitive documents or source records.

Risk: The free edition lists checks that are not run, so users may overestimate coverage.

Mitigation: Show executed checks and checks not run in the output, and avoid presenting a clean result as coverage beyond the stated free-edition checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/rd-auxiliary-ledger-check-free)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable console text or JSON validation results from a local Node.js command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include severity, category, message, cited evidence, summary counts, executed checks, and checks not run.]

## Skill Version(s):

1.0.16 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
