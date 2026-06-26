## Description: <br>
Extract structured data from invoices and receipts, output JSON or CSV, and maintain a running expense ledger. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[99rebels](https://clawhub.ai/user/99rebels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Freelancers, small businesses, contractors, and their agents use this skill to extract invoice and receipt fields, categorize expenses, review entries, and export or maintain a CSV ledger for accounting and tax preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write, edit, delete, undo, and export local financial ledger data. <br>
Mitigation: Review extracted entries before adding them and explicitly confirm edit, delete, undo, and export actions. <br>
Risk: Exported CSV files can contain sensitive financial data. <br>
Mitigation: Avoid exporting to shared or public paths and choose output locations deliberately. <br>
Risk: New export presets can change how ledger fields are written to expense-config.json and exported CSVs. <br>
Mitigation: Review any newly discovered export preset before allowing the agent to save it. <br>


## Reference(s): <br>
- [Configuration Reference](references/configuration.md) <br>
- [Platform Formatting Examples](references/formatting.md) <br>
- [Implementation Notes](references/notes.md) <br>
- [Invoice Extractor Product Plan](references/product-plan.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, CSV, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON, CSV, and shell command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces extracted invoice fields, ledger entries, expense summaries, export files, and user confirmation prompts.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
