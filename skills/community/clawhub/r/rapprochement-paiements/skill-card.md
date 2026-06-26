## Description: <br>
Rapproche les opérations bancaires avec les factures et notes de frais, signale les paiements réglés, partiels, impayés ou en retard, et produit un suivi mensuel par client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trendex](https://clawhub.ai/user/trendex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accountants and finance operators use this skill to reconcile client bank transactions against classified invoices and expense reports. It highlights missing invoices, orphan payments, duplicate payments, unreadable statements, overdue invoices, and documents that need visual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive bank, invoice, and expense data may be persisted in plaintext transcriptions, extraction caches, and vision sidecars beside accounting documents. <br>
Mitigation: Run the skill only in a controlled copy or secured accounting workspace, review generated files, and define cleanup and retention rules for all generated artifacts. <br>
Risk: Accounting follow-up can be affected if generated matches, anomalies, or visual-review corrections are accepted without review. <br>
Mitigation: Review reconciliation output, unresolved vision items, duplicate-payment flags, and overdue-invoice recommendations before relying on them or sending reminders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/trendex/rapprochement-paiements) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown instructions with command examples and JSON reconciliation artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes per-client reconciliation state, consolidated reports, review queues, and document extraction sidecars.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
