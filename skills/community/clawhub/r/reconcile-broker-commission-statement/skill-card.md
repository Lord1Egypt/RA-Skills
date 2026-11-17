## Description:

Reconcile broker commission statements against expected loan-level payouts, flag variances, and provide a detailed summary with recommended follow-up actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li-chi](https://clawhub.ai/user/li-chi)

### License/Terms of Use:

MIT-0

## Use Case:

Finance operations and payout teams use this skill to reconcile broker, lender, or internal commission statements against expected loan-level commissions before payment approval or variance follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commission statements and loan-level exports can contain sensitive financial and personal information.

Mitigation: Provide only the fields needed for reconciliation, redact unnecessary personal identifiers where possible, and follow approved storage, access, and retention procedures.

Risk: Ambiguous matches, unclear gross-versus-net basis, fees, clawbacks, or poor OCR quality can produce misleading reconciliation results.

Mitigation: Mark uncertain rows as needs_review, preserve an audit trail in notes, call out totals that do not foot, and request missing plan or statement details before approving payout actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/li-chi/skills/reconcile-broker-commission-statement)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with reconciled tables, summary bullets, status labels, variance amounts, and recommended next actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses provided statement and expected payout data; preserves notes for ambiguous matches, adjustments, and low-confidence extraction.]

## Skill Version(s):

1.2.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
