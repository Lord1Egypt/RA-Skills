## Description:

版税与授权金结算核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。触发词包括 版税与授权金结算核对、版税与授权金结算核对表对不上。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Copyright accounting, royalty operations, and business teams use this skill to check royalty and licensing settlement tables before issuing statements or during audit sampling. It recomputes row arithmetic, verifies totals, detects duplicates or blank placeholders, and cites source rows for each finding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Settlement tables may contain sensitive royalty, licensing, or business data.

Mitigation: Run the checker locally and provide only the settlement table content intended for analysis.

Risk: The free version omits several advanced contract, rate, and prepaid-royalty checks.

Mitigation: Treat results as arithmetic and reconciliation checks only; review omitted contract, tier-rate, and prepaid-royalty issues separately.

Risk: Users who cannot review Chinese-language output may misread findings or limits.

Mitigation: Use this release only when the operator can understand the Chinese documentation and checker output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/royalty-settlement-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable Chinese text or JSON from a local Node.js checker]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows when available; insufficient input produces no conclusion rather than a false clean result.]

## Skill Version(s):

1.0.46 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
