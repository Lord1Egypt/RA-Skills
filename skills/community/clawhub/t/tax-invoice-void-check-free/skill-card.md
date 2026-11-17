## Description:

Checks invoice void and reversal ledgers by recomputing row arithmetic, totals, duplicate invoice numbers, missing required values, and negative amounts, with findings tied to source rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, and tax operations users use this skill during monthly closing, reconciliation, or inventory checks to validate an invoice void and reversal ledger before relying on it. It is limited to the free checks declared by the skill and does not provide broader tax compliance determinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server scan reports a contradiction around a tax/declaration-form revenue difference check that the free package does not actually perform.

Mitigation: Treat results as limited ledger arithmetic checks only; do not rely on this skill for declaration-form revenue difference validation or broader tax compliance unless the publisher fixes the contradiction and implements or removes the claimed check.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/tax-invoice-void-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable text or JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows; insufficient input produces missing-field guidance instead of a pass/fail conclusion.]

## Skill Version(s):

1.0.57 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
