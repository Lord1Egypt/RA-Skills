## Description:

Checks copied utility allocation tables for row arithmetic, column totals, duplicate tenants, and blank or placeholder values, with each finding citing the source line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, and property operations users use this skill during monthly reconciliation to check pasted utility allocation tables before billing or settlement. It flags arithmetic mismatches, total-row errors, duplicate tenants, and missing or placeholder values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Node script on copied utility allocation table text.

Mitigation: Install and run it only when local script execution is acceptable, and review the clean ClawHub security summary before deployment.

Risk: The free release omits several allocation checks, including share-to-amount consistency, invalid share percentages, negative payable totals, and tenant share-to-area consistency.

Mitigation: Treat a passing result as limited to the executed free checks, and use separate review for the omitted allocation checks when they matter.

Risk: The skill does not read Excel files directly and requires copied table text with recognizable headers.

Mitigation: Export or copy the table with headers into text or JSON before running, and do not rely on the skill to infer conclusions from insufficient input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/utility-allocation-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text or JSON findings with source line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on copied table text; returns insufficient-input guidance instead of conclusions when required table evidence is missing.]

## Skill Version(s):

1.0.47 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
