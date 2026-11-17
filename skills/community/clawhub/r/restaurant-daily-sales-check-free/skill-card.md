## Description:

Checks restaurant daily sales report tables by recalculating row totals, cross-checking summary totals, and flagging duplicate, blank, placeholder, or negative-value entries with source-backed findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance staff, cashiers, store managers, and operations reviewers use this skill to check restaurant daily sales report tables during settlement, reconciliation, or inventory-close workflows. It helps identify arithmetic and consistency issues in the submitted table, while withholding conclusions when required table material is missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads restaurant sales report files supplied by the user.

Mitigation: Run it only on files you are comfortable processing locally, and avoid providing unrelated sensitive material.

Risk: The checker is not a full financial audit and does not cover all settlement, tax, refund, cross-day, or platform-policy issues.

Mitigation: Use the output as a table arithmetic and consistency check, then review unresolved accounting questions with the responsible finance process.

Risk: The free release omits several disclosed checks, including platform-fee validation and some overcollection or policy-range checks.

Mitigation: Review the listed checks_not_run or withheld checks before relying on the result for final reconciliation decisions.

Risk: The tool withholds conclusions when table material is missing or cannot be parsed.

Mitigation: Provide the report with headers and required columns, and treat insufficient-input output as a request for better source material rather than as a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/restaurant-daily-sales-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [analysis, json, text, shell commands, guidance]

**Output Format:** [Human-readable text or JSON containing executed checks, findings, summary, omitted checks, and scope notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against user-provided restaurant sales table text; exits with a distinct insufficient-input status instead of issuing a no-issue conclusion when required material is missing.]

## Skill Version(s):

1.0.47 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
