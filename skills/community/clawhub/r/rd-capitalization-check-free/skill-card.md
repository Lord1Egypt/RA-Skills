## Description:

研发支出明细表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, accounting, audit-preparation, and tax operations users can run this local checker on R&D expenditure detail tables before month-end close, annual settlement, or audit review. It checks arithmetic consistency, totals, duplicate rows, blanks, and missing required columns while leaving accounting, tax, and audit judgments to qualified reviewers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic screening results as audit, tax, or accounting advice.

Mitigation: Treat the output as a screening aid and have qualified reviewers confirm accounting treatment, tax eligibility, audit conclusions, and source-table completeness.

Risk: Incomplete or malformed R&D expenditure tables can lead to missing or unreliable checks.

Mitigation: Verify that inputs include the required table headers and relevant columns, especially cumulative capitalization, amortization, and ending intangible asset balance, before relying on a no-issue result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/rd-capitalization-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON checker results, with Markdown command examples in the skill instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided R&D expenditure table text; no network or persistence is reported by the security evidence.]

## Skill Version(s):

1.0.19 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
