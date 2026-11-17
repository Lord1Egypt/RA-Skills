## Description:

Recite processes receipt images and PDFs with the Recite Vision API, renames files by extracted date and vendor data, and records transaction details in a CSV ledger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rivradev](https://clawhub.ai/user/rivradev)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Recite to process folders of receipts or invoices, extract transaction fields through the Recite API, rename source files, and maintain a bookkeeping CSV for expense and tax workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipt and invoice contents are sent to the Recite remote API.

Mitigation: Install only when this data transfer is acceptable, use a restricted receipt folder, and keep backups before processing files.

Risk: The skill uses extracted API data to rename files and populate a spreadsheet-compatible CSV.

Mitigation: Review generated filenames and treat the CSV as untrusted before opening it in spreadsheet software.

Risk: The skill requires a Recite API key stored in an environment variable or local configuration file.

Mitigation: Prefer an environment variable or protected secret store and avoid committing local configuration containing the API key.

## Reference(s):

- [Recite skill page](https://clawhub.ai/rivradev/skills/recite)
- [rivradev publisher profile](https://clawhub.ai/user/rivradev)
- [Recite API key settings](https://recite.rivra.dev/settings/api)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands; script execution writes renamed files and a CSV ledger.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates bookkeeping_transactions.CSV in the target folder and renames processed receipt, invoice, and PDF files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
