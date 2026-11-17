## Description:

税务风险指标自查核对（免费版）本地复算税务风险指标自查表中的税负率、进销项比和合计行，并检测重复、空缺、占位符和负数金额。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

Proprietary

## Use Case:

Finance and accounting staff use this skill during monthly or quarterly closing, reconciliation, and tax self-check workflows to validate a Chinese tax risk indicator table before relying on it. It reports deterministic arithmetic and consistency findings with source row references, and reports insufficient input instead of inventing conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the free subset as a full tax risk assessment.

Mitigation: Confirm the executed checks and withheld checks in the output before relying on results.

Risk: The checker may be unable to evaluate malformed or incomplete table input.

Mitigation: Provide the required table headers and period rows; when input is insufficient, treat the result as no conclusion rather than no issue.

Risk: Tax indicators can depend on local rules, industry context, and professional judgment.

Mitigation: Use findings as arithmetic and consistency checks, then review material issues with the applicable tax authority guidance or a qualified tax professional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/tax-riREDACTED-SECRET)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text or JSON results from a local Node.js checker]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows; the free version lists checks that were executed and checks that were not run.]

## Skill Version(s):

1.0.47 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
