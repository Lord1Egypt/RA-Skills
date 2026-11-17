## Description:

税收优惠适用条件自查表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and tax staff use this skill to locally check Chinese tax incentive self-check tables for arithmetic consistency, totals, duplicate rows, blanks, and negative values. Its findings support reconciliation review and should not be treated as tax or legal eligibility advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat reconciliation findings as tax or legal eligibility advice.

Mitigation: Present results as table arithmetic and consistency checks, and require review against current rules and the relevant tax authority position before acting.

Risk: The local runner reads an input path supplied by the user.

Mitigation: Only run it on files intentionally prepared for this check and avoid pointing it at unrelated sensitive files.

Risk: The free edition omits several checks and does not issue conclusions when input is insufficient.

Mitigation: Do not interpret a lack of findings as complete tax incentive eligibility; review the omitted checks and provide complete table data when running the tool.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/tax-incentive-eligibility-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON check results with cited source lines and missing-input guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js on user-provided files; no network access, persistence, credential use, or hidden side effects were reported by the security evidence.]

## Skill Version(s):

1.0.46 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
