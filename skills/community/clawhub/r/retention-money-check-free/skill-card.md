## Description:

A Chinese-language local checker for construction retention-money ledgers that recomputes withheld amounts, warranty-expiry dates, refundable amounts, total rows, duplicate settlement IDs, blanks, and unrecognized dates with source ledger line citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Project accountants, cost staff, construction contractors, and owner-side infrastructure finance teams use this skill to check construction retention-money ledgers during settlement close, final-account reconciliation, and warranty-period refund review. It is intended for arithmetic and ledger consistency checks, not legal entitlement or overdue-refund determinations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic ledger findings as legal or contractual determinations.

Mitigation: Use the output only for local arithmetic and consistency checks; review contract terms, legal entitlement, overdue refund status, deduction reasonableness, interest, and cap compliance separately.

Risk: The free version omits several refund, deduction, and contract-cap checks.

Mitigation: Confirm the executed and withheld check lists in the output before acting, and do not infer that omitted checks passed.

Risk: Incomplete or malformed ledger input can produce no conclusion rather than a finding.

Mitigation: Provide a table with headers and the required fields before relying on results; treat insufficient-input responses as unresolved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/retention-money-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable text or JSON report with findings, missing-input messages, executed checks, withheld checks, and ledger line references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally through the bundled Node.js checker; no network use is reported in the security evidence.]

## Skill Version(s):

1.0.53 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
