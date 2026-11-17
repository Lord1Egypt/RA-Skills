## Description:

仓储费结算表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Business operations teams and finance reviewers use this skill to check monthly warehouse-fee and overdue-fee settlement tables. It recalculates stated charges, reviews totals, flags duplicate or missing rows, and cites source line numbers for each finding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free release omits several validation checks, including negative rates, non-positive quantities, extreme day counts, overdue days exceeding billed days, and negative or below-storage totals.

Mitigation: Treat results as coverage for the executed checks only, and review the omitted-check list before relying on the output.

Risk: The skill is not a full contract, rate-card, or legal review.

Mitigation: Confirm fee rates, free-storage-period treatment, and contractual obligations against the governing documents.

Risk: Input tables without recognizable headers or enough detail do not support a reliable conclusion.

Mitigation: Provide a warehouse-fee settlement table with headers and line items; when input is insufficient, use the reported missing-materials list before rerunning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/warehouse-fee-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable text or JSON with findings, summaries, executed checks, and omitted checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers; insufficient input returns missing materials instead of a pass/fail conclusion.]

## Skill Version(s):

1.0.31 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
