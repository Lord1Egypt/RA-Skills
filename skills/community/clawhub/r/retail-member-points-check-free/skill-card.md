## Description:

A free local checker for member points and stored-value card reconciliation tables that recalculates row balances, totals, duplicates, blanks, and negative values with source-cited findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, and retail operations users run this skill during monthly closing, reconciliation, or inventory checks to verify member points and stored-value card tables. It helps identify arithmetic mismatches, total-row errors, duplicate member-period rows, missing required cells, and negative transaction values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker only evaluates the provided table and does not replace accounting, tax, or compliance judgment.

Mitigation: Use it as a reconciliation aid and route accounting, tax, regulatory, or recognition-policy questions to qualified reviewers.

Risk: The free release intentionally omits several checks that may matter for a complete retail reconciliation.

Mitigation: Review the listed checks_not_run and checks_out_of_scope before relying on the result for close or audit workflows.

Risk: Input tables may contain customer or member data.

Mitigation: Provide only the specific reconciliation table needed for the check and avoid unnecessary personal or sensitive fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/retail-member-points-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown-style guidance and command examples, with optional structured JSON results from the local runner]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows and include executed checks, withheld checks, summary counts, and out-of-scope notes.]

## Skill Version(s):

1.0.51 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
