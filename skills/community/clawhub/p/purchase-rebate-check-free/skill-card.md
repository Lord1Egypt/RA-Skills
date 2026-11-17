## Description:

采购返利核对表逐项核对（应得返利与差额复算、合计勾稽、重复与空缺检测），每条结论引用原文行号。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, finance, and operations users can use this skill to check supplier purchase-rebate tables for rebate recalculation errors, difference recalculation errors, total-row mismatches, duplicate suppliers, and blank or placeholder fields. It is intended for local review support and does not replace contract, tax, accounting, or final financial judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free tier omits bracket-rate validation, rate range checks, negative-value checks, and threshold-based difference checks.

Mitigation: Independently verify omitted checks and contract-specific rebate terms before making final financial decisions.

Risk: The skill does not provide tax, accounting, contract interpretation, or final financial advice.

Mitigation: Use the output as review support and have qualified personnel confirm material conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/purchase-rebate-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable text or JSON result object with executed checks, omitted checks, status, and line-cited findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js; the free tier reports the checks it executes and the checks it omits.]

## Skill Version(s):

1.0.32 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
