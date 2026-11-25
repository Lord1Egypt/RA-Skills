## Description:

For anyone who must turn screenshots, scans, PDF captures, and phone photos of paper tables into usable data, the skill combines vision semantics, OCR coordinates, and programmatic checks to produce Excel, CSV, or JSON with a verification report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengjianli0721](https://clawhub.ai/user/fengjianli0721)

### License/Terms of Use:

MIT-0

## Use Case:

External users and data analysts use the skill to turn screenshots, scans, PDFs, and phone photos of structured tables into auditable spreadsheets or structured data, with checks for merged cells, checkboxes, continued pages, and numeric consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File access may extend beyond the inputs and outputs intended for a run.

Mitigation: Review file access and output paths, and use the skill only with files appropriate for processing.

Risk: Numeric parsing can misread negative, qualified, or comma-grouped values and affect the extracted data.

Mitigation: Check those values against the source image and confirm the totals and verification report before relying on the output.

## Reference(s):

- [ClawHub release](https://clawhub.ai/fengjianli0721/skills/tablescribe)
- [Extraction playbook](references/extraction-playbook.md)
- [Cell reconstruction](references/cell-reconstruction.md)
- [Verification rules](references/verification-rules.md)
- [Failure modes](references/failure-modes.md)

## Skill Output:

**Output Type(s):** [Files, Excel spreadsheets, CSV, JSON, Markdown]

**Output Format:** [XLSX workbook, CSV or JSON table, with a verification report and reconstruction note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a column dictionary, verification results, and notes for doubts or skipped items.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
