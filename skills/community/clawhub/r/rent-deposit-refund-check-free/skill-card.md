## Description:

A local CLI skill that checks rent and security deposit collection and refund ledgers for refund math, deduction basis and limits, overdue refunds, duplicate refunds, ledger balance reconciliation, missing fields, and negative amounts with source row citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, treasury, property operations, and leasing teams use this skill to review deposit ledgers before refunds, month-end reconciliation, or follow-up on unsettled balances. It is designed for user-supplied tabular text and returns advisory findings that should be checked against contracts, bank records, receipts, and internal policy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill output is advisory and may be incomplete or inappropriate for a specific refund decision if contracts, bank records, receipts, or internal policies differ from the supplied ledger text.

Mitigation: Verify findings against contracts, bank records, receipts, and internal policy before taking business action.

Risk: The free release does not perform every possible deposit review, including legality of deductions, proof of payment, interest, tax, invoice handling, or cross-period aggregation.

Mitigation: Use the reported scope and out-of-scope checks to decide whether additional manual review or a fuller workflow is required.

Risk: The tool expects Chinese-language ledger fields and may return insufficient-input results when required columns or recognizable headers are missing.

Mitigation: Provide the required ledger columns with clear headers, or first run the bundled sample to match the expected input shape.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/rent-deposit-refund-check-free)
- [Skill documentation](artifact/SKILL.md)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Human-readable CLI text or structured JSON with findings, summary, scope, missing-input advice, and source row citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; findings are advisory and materials are insufficient when required columns are missing.]

## Skill Version(s):

1.0.5 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
