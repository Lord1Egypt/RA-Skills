## Description:

Identify recurring charges and subscriptions from receipts or email exports, and produce a clean summary with renewal dates, price changes, and cancellation drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codedao12](https://clawhub.ai/user/codedao12)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to audit receipts, billing PDFs, CSVs, or email exports for recurring charges, renewal dates, price changes, overlapping subscriptions, and potential savings. It produces summaries, reminder recommendations, and cancellation drafts without initiating payments, cancellations, disputes, or messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipts, billing PDFs, CSVs, and email exports can contain sensitive personal, address, or payment-adjacent information.

Mitigation: Prefer offline exports, keep data local to the user workspace, redact full card numbers and addresses, and avoid storing raw receipts outside the workspace.

Risk: Optional email, IMAP, OCR, or webhook inputs may expose account data or untrusted inbound content.

Mitigation: Use read-only scopes only when account access is explicitly needed, treat inbound data as untrusted, and sanitize inputs before parsing.

Risk: Draft reminders or cancellation messages could be inaccurate or sent before review.

Mitigation: Generate drafts and schedules only; require the user to manually review and send any message themselves.

## Reference(s):

- [Receipt Subscription Cleaner on ClawHub](https://clawhub.ai/codedao12/skills/receipt-subscription-cleaner)
- [Overview](references/overview.md)
- [Auth](references/auth.md)
- [Endpoints](references/endpoints.md)
- [Safety](references/safety.md)
- [Troubleshooting](references/troubleshooting.md)
- [UX](references/ux.md)
- [Webhooks](references/webhooks.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables, lists, and draft message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confidence labels, anomaly notes, renewal estimates, reminder recommendations, and drafts only; no payment, cancellation, dispute, or sending action is performed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
