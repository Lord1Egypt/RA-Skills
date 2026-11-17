## Description:

Checks copied social-insurance and housing-fund declaration tables for row-level arithmetic, total reconciliation, duplicate people, and missing placeholders, with findings tied to source line numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, payroll, cashiering, warehouse, and operations staff use this skill during monthly closing, payroll, reconciliation, or inventory workflows to check pasted social-insurance declaration details before downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic reconciliation output as legal, tax, audit, or policy advice.

Mitigation: Use the skill only for local table checking and require qualified review before making legal, tax, audit, payroll-policy, or filing decisions.

Risk: The free version omits ratio, base-limit, eligibility, and base-consistency checks.

Mitigation: Review the withheld-check list in the output and do not interpret a clean free-version result as full social-insurance or housing-fund compliance.

Risk: Incomplete or unrecognized input tables can prevent meaningful checking.

Mitigation: Provide copied table text with headers and source rows; when the skill reports insufficient input, collect the missing fields before relying on any result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/social-insurance-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [analysis, markdown, json, shell commands, guidance]

**Output Format:** [Human-readable console report or JSON result with executed checks, withheld checks, findings, missing inputs, and source-line references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on copied table text; the free version excludes ratio, base-limit, eligibility, and personal-versus-employer base consistency checks.]

## Skill Version(s):

1.0.53 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
