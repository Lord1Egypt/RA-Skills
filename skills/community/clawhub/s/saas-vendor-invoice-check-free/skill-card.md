## Description:

Checks a SaaS vendor invoice and usage-detail table by recomputing billed amounts, comparing billable quantities with usage or seats, tying total rows, detecting duplicate charges, flagging prices above contract price, and reporting blank key fields with source line references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, finance, and IT asset teams use this skill during monthly vendor billing, quarterly usage review, and renewal preparation to reconcile SaaS invoices against usage or seat detail before payment or negotiation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive billing and usage records.

Mitigation: Run it locally as provided, avoid unnecessary sharing of input files, and confirm that processing remains local before using real vendor data.

Risk: Invoice findings can affect payment or vendor negotiation decisions.

Mitigation: Verify findings against contracts, vendor systems, internal usage records, and seat inventories before acting.

Risk: The free version withholds several advanced checks and may miss issues outside its stated scope.

Mitigation: Review the reported checks not run and do not treat a clean result as proof that the invoice has no other problems.

Risk: Missing or blank required fields can otherwise lead to misleading reconciliation assumptions.

Mitigation: Use the insufficient-input response to complete missing columns or values instead of substituting defaults.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/saas-vendor-invoice-check-free)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers and service identifiers; insufficient input returns missing-field guidance instead of a positive conclusion.]

## Skill Version(s):

1.0.5 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
