## Description:

A local ticket revenue and channel settlement checker that recomputes row-level ticket revenue, commission, refund, settlement, duplicate-order, missing-field, placeholder, negative-value, and total-row arithmetic from user-supplied settlement tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External finance and ticket-settlement teams use this skill to check monthly ticket revenue and channel settlement sheets before confirming revenue or paying channels. It is limited to arithmetic reconciliation inside the submitted table and does not verify box-office authenticity, bank receipts, contract terms, or tax treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker can miss real-world issues outside the submitted table, including box-office authenticity, bank receipts, contract terms, and tax treatment.

Mitigation: Use the output only as an arithmetic reconciliation aid, and verify external facts against ticketing, banking, contract, and tax records before making financial or legal decisions.

Risk: Incomplete or malformed settlement data can lead to no conclusion or findings that only cover the supplied rows.

Mitigation: Provide the required table headers and source rows, and treat any clean result as limited to the data submitted for that run.

Risk: Ticket revenue and channel settlement data may be commercially sensitive even when processing is local.

Mitigation: Run the Node-based checker in a trusted local environment and avoid exposing confidential input data in prompts, logs, or shared output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/ticket-revenue-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Human-readable reconciliation findings, with optional JSON output from the runner.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include line numbers, categories, advice, executed checks, withheld checks, and explicit out-of-scope boundaries.]

## Skill Version(s):

1.0.5 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
