## Description:

个税汇算清缴助手。支持年终奖与期权双重单独/合并计税决策优化，智能分析多雇主重复起征点与税率跳档，生成个税 APP 申报实操指南。

This skill is ready for commercial/non-commercial use.

## Publisher:

[afeicn](https://clawhub.ai/user/afeicn)

### License/Terms of Use:

MIT-0

## Use Case:

External taxpayers or tax advisors use this skill for China individual income tax annual settlement planning. It compares annual bonus and equity incentive filing choices, explains likely refund or payment outcomes, and provides steps for the individual income tax app.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill may process sensitive tax records, income details, deductions, prepayments, and filing choices.

Mitigation: Prefer manual entry over screenshots, redact personal identifiers and unrelated details, and share only the tax fields needed for the calculation.

Risk: Filing recommendations could be wrong if user-provided amounts, deductions, prepayments, or filing choices are incomplete or inaccurate.

Mitigation: Verify all income, deductions, prepayments, and filing choices against official records before submitting anything in the tax app.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with comparison tables, filing recommendations, and app filing steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided tax inputs; no persistent output files are expected.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
