## Description:

Extracts transaction and table rows from bank, card, brokerage, invoice, and vendor price-list PDFs into CSV or Excel, then checks the rows against printed balances, totals, counts, and number formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bankgpt](https://clawhub.ai/user/bankgpt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance operations teams use it to turn statement and invoice PDFs into traceable spreadsheet rows and identify missing or inconsistent data before bookkeeping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was benign but partial and identified gaps in verification claims, so an extraction may not establish completeness in every case.

Mitigation: Review proof reports and source-page traceability before bookkeeping, and investigate failed checks rather than forcing a tie-out.

## Reference(s):

- [Formats and statement layouts](artifact/references/formats.md)
- [OCR guidance for scanned statements](artifact/references/ocr.md)
- [ClawHub release page](https://clawhub.ai/bankgpt/skills/statement-extract-and-prove)

## Skill Output:

**Output Type(s):** [Files, Analysis]

**Output Format:** [CSV or XLSX transaction tables, Markdown proof reports, and JSON proof metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rows include page and vertical-position traceability; low-confidence rows and unassigned lines are reported.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
