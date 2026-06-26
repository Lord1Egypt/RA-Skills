## Description: <br>
Identifies recurring charges and subscriptions from receipts or email exports, producing a clean summary with renewal dates, price changes, and cancellation drafts for spending audits without initiating payments or cancellations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to audit receipts, email exports, PDFs, or CSV lists for recurring charges, renewal estimates, anomalies, draft cancellation messages, and reminder schedule recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt data may include sensitive fields such as payment card details or addresses. <br>
Mitigation: Redact sensitive fields in outputs and avoid storing raw receipts outside the user workspace. <br>
Risk: Draft cancellation emails or reminder guidance could be mistaken for completed subscription actions. <br>
Mitigation: Keep actions read-only, do not send emails or perform cancellations, and require the user to review any draft before use. <br>
Risk: Optional account or email access can expose private receipt data if broad permissions are used. <br>
Mitigation: Prefer offline exports and use read-only scopes only when API access is explicitly requested. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/codedao12/receipt-subscription-cleaner) <br>
- [Overview](references/overview.md) <br>
- [Auth](references/auth.md) <br>
- [Endpoints](references/endpoints.md) <br>
- [Safety](references/safety.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [UX](references/ux.md) <br>
- [Webhooks](references/webhooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown with subscription tables, anomaly lists, draft email templates, and reminder recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only output; drafts are not sent and payment or cancellation actions are out of scope.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
