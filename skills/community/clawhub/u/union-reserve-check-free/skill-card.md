## Description:

工会经费与残保金计提表逐项核对，每条结论都带原文依据，不需要付款，也不需要注册。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting users use this skill during monthly close, reconciliation, or stocktaking to check union-fund and disability-fund accrual tables for row-level arithmetic, total tie-outs, duplicate periods, blanks, and placeholder values. It returns cited findings and withholds conclusions when required table evidence is missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free edition omits several listed checks, including rate-range alerts, additional remittance bounds, disability-fund reconciliation, and retained-amount checks.

Mitigation: Review the displayed checks_not_run and do not treat omitted checks as passed; use a fuller review process when those checks are required.

Risk: Accounting conclusions depend on complete, recognizable table headers and source rows.

Mitigation: Provide the table with required headers and review missing-field output; when materials are insufficient, the skill should return no conclusion.

Risk: The tool is a Chinese-language local CLI for a specific accounting table and may be misread by users unfamiliar with the terminology.

Mitigation: Have a finance reviewer who can read the Chinese source table and output verify findings before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/union-reserve-check-free)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON]

**Output Format:** [Human-readable text or structured JSON from a local CLI run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; accepts a JSON or plain-text table input and reports missing evidence instead of fabricating conclusions.]

## Skill Version(s):

1.0.46 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
