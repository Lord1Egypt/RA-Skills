## Description: <br>
Analyzes pre-classified client accounting folders, reconciles invoices with bank transactions, validates VAT, and produces follow-up, reminder, anomaly, and consolidated report JSON for accountants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trendex](https://clawhub.ai/user/trendex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accounting firm staff use this skill to run a deterministic reconciliation batch over client folders, then review payment status, overdue invoices, reminders, VAT issues, and blocking anomalies before taking accounting or follow-up action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads sensitive invoices and bank statements from client accounting folders. <br>
Mitigation: Install it only in an accounting workspace where the agent is authorized to access those documents and run it only against the intended clients directory. <br>
Risk: Generated reconciliation, VAT, anomaly, and reminder outputs may be incomplete or incorrect if source documents are missing, malformed, or poorly extracted. <br>
Mitigation: Review followup.json, relances.json, anomalies.json, and the consolidated report before relying on reminders or accounting decisions. <br>
Risk: PDF extraction depends on the pdftotext runtime dependency. <br>
Mitigation: Install poppler-utils from a trusted package source and surface the exact script error if extraction or batch execution fails. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/trendex/rapprochement-bancaire) <br>
- [Companion organisation-documents skill](https://github.com/developers-trendex/organisation-documents) <br>
- [CSV schema reference](references/csv-schema.md) <br>
- [Matching rules reference](references/matching-rules.md) <br>
- [Target folder structure reference](references/structure-cible.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON files, Guidance] <br>
**Output Format:** [Markdown summary with shell command context and JSON report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The batch writes followup.json, relances.json, anomalies.json, per-period lock files, and a consolidated compta_batch_report_<date>.json; the agent relays a concise accountant-facing summary.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
