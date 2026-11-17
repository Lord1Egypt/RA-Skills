## Description:

餐饮菜品成本与出品率核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Restaurant finance and operations staff use this skill to check copied dish cost and yield tables before monthly reconciliation, cost review, or inventory close. It checks table arithmetic, total-line consistency, duplicate rows, blank placeholders, and negative values, while citing source rows for findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free release intentionally omits checks such as yield-range alerts, variance-rate alerts, and source-record truth validation.

Mitigation: Use the output as a table-consistency check and review the disclosed omitted checks before relying on it for broader restaurant cost or yield decisions.

Risk: Incorrect or incomplete copied table input can lead to missing checks or no conclusion.

Mitigation: Provide the table with headers and source rows; when the skill reports insufficient input, correct the input rather than treating the absence of findings as clearance.

Risk: The skill does not validate whether kitchen, inventory, POS, tax, or source accounting records are accurate.

Mitigation: Confirm source records and accounting policy decisions with the responsible restaurant operations or finance reviewers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/restaurant-food-cost-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable text or JSON findings with source-row references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided table text and reports insufficient input instead of making unsupported conclusions.]

## Skill Version(s):

1.0.47 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
