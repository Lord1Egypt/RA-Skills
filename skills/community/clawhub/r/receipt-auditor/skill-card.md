## Description: <br>
Extract, categorize, and audit receipts and bills to generate expense reports and spot discrepancies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, freelancers, groups, and household finance users use this skill to turn raw receipt or bill text into categorized expense reports, AA split calculations, and anomaly-focused bill audits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Receipt, credit-card, reimbursement, or travel details may be saved locally in references/last-prompt.txt when the CLI builds the assistant prompt. <br>
Mitigation: Use redacted test data, avoid sensitive real receipts unless this local save behavior is acceptable, or remove/change the prompt-saving behavior before operational use. <br>
Risk: Generated expense categories, anomaly flags, and AA split totals may be wrong or incomplete for ambiguous bill text. <br>
Mitigation: Manually verify parsed line items, categories, totals, anomaly warnings, and AA split reconciliation before submitting reports or requesting reimbursement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/receipt-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/harrylabsj) <br>
- [Expense categories](references/categories.json) <br>
- [Input schema](schemas/input.schema.json) <br>
- [Output schema](schemas/output.schema.json) <br>
- [Report template](references/templates/report-template.md) <br>
- [AA split template](references/templates/aa-split-template.md) <br>
- [Audit template](references/templates/audit-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and tables, JSON-compatible schemas, and shell command prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports report, aa-split, and audit modes with CNY default currency and zh/en output language options.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
