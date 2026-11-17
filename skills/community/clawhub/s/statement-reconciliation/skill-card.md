## Description:

Check a vendor statement against the AP log to confirm every invoice is recorded, and draft a request for any that are missing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skillsandagentsco](https://clawhub.ai/user/skillsandagentsco)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting, finance, and operations users use this skill when a vendor statement arrives to compare it against AP records, identify missing invoices, and prepare a reviewed vendor request when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes vendor statements and accounts-payable logs that may contain sensitive financial records.

Mitigation: Use only AP logs and vendor statements the operator is authorized to process.

Risk: A missing-invoice request sent to a vendor can create an irreversible external communication.

Mitigation: Keep the default draft-only behavior and require a human to review and send any vendor reply.

Risk: Undefined match tolerance can lead to loose or inconsistent invoice matching.

Mitigation: Define invoice number, date, and amount tolerance in plan mode before running the reconciliation.

Risk: Ambiguous, unreadable, or near-match statement lines can be mistaken for confirmed matches or true missing invoices.

Mitigation: List ambiguous lines separately as confirm items and review them before closing the reconciliation or contacting the vendor.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/skillsandagentsco/skills/statement-reconciliation)
- [Statement Reconciliation documentation](https://skillsandagents.co/skills/statement-reconciliation/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with reconciliation status, cited matched lines, missing-invoice list, confirm list, and drafted vendor reply when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Vendor replies are drafted only and require human review before sending.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
