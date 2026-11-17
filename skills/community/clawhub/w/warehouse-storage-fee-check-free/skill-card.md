## Description:

A free deterministic checker for warehouse storage-fee settlement statements and inventory-aging detail, with line-cited findings for six table-level checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Warehouse, logistics, and finance staff use this skill before payment to check settlement tables for arithmetic mismatches, missing fields, duplicate rows, negative values, and fee-day inconsistencies. The skill reports source line numbers and withholds conclusions when the input material is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial findings may be mistaken for final payment instructions.

Mitigation: Treat findings as review leads and confirm payment, adjustment, and contract decisions with the responsible finance or operations process.

Risk: The interface, sample data, and output are Chinese-language, which may affect reviewers who do not read Chinese.

Mitigation: Have a Chinese-reading reviewer confirm input mapping, findings, and withheld checks before relying on the results.

Risk: The free version intentionally omits several checks that are listed as withheld.

Mitigation: Review the reported scope and withheld checks before deciding whether additional reconciliation is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/warehouse-storage-fee-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable Chinese text or a JSON result object containing status, findings, summary, scope, and disclaimer fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers; insufficient input returns missing requirements instead of a pass/fail conclusion.]

## Skill Version(s):

1.0.5 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
