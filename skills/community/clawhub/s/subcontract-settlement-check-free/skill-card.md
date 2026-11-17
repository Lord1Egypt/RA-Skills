## Description:

分包结算与产值核对（免费版） locally checks subcontract settlement tables for row arithmetic, totals, duplicate entries, blanks, and negative values, with findings tied to source evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashiering, and operations teams use this skill during monthly settlement, reconciliation, and close processes to check subcontract settlement tables before downstream payment or review. It helps identify arithmetic mismatches, duplicate rows, blank placeholders, and negative amount entries while avoiding unsupported conclusions when inputs are incomplete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subcontract settlement inputs may contain confidential financial or counterparty data.

Mitigation: Use a purpose-specific input file and avoid including unrelated confidential records.

Risk: Incomplete or malformed tables can produce unsupported settlement conclusions if treated as complete records.

Mitigation: Rely on the skill's insufficient-input response and provide the missing table headers or rows before using results in a payment workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/subcontract-settlement-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON reports with cited source rows; usage guidance may include shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are generated from local input files; insufficient input returns missing requirements instead of a settlement conclusion.]

## Skill Version(s):

1.0.56 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
