## Description:

返利台账逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文，并只执行免费版声明的本地检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Sales finance and commercial teams use this skill before monthly accruals or quarterly/year-end rebate payouts to check exported rebate ledgers for formula, roll-forward, total, duplicate-row, negative-value, and blank-field issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat rebate-ledger findings as accounting, audit, tax, or legal advice.

Mitigation: Use the skill as a local consistency check only; qualified reviewers should make policy, recognition, audit, and tax decisions.

Risk: The free edition does not run every rebate-control check described by the broader product family.

Mitigation: Review the omitted-check notices in the output and perform material omitted checks separately before relying on the ledger.

Risk: The checker expects exported ledger text with recognizable headers and does not connect directly to business systems.

Mitigation: Provide headered ledger text or JSON input from a trusted export and verify source completeness before using the results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/sales-rebate-check-free)
- [Sample input template](artifact/templates/sample.json)
- [Skill source summary](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable CLI text or JSON results with findings, summaries, scope, and omitted-check notices.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs deterministic local Node.js checks; insufficient input returns missing requirements rather than a ledger conclusion.]

## Skill Version(s):

1.0.17 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
