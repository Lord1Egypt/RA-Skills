## Description:

车辆保险与保费摊销核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and bookkeeping users use this skill during monthly close, reconciliation, or inventory checks to verify vehicle insurance premium amortization tables. It recalculates row-level amortization, checks totals, detects duplicate or missing entries, and cites source rows for each finding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker reads user-supplied vehicle insurance amortization tables from local files.

Mitigation: Use it only with tables the user intends the local Node script to read.

Risk: Negative-amount findings may need careful review for cancellation or endorsement reversals.

Mitigation: Review negative-amount findings against the original table and business context before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/vehicle-insurance-amortization-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text or JSON check results with cited findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-supplied table input and reports insufficient materials without issuing a conclusion.]

## Skill Version(s):

1.0.48 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
