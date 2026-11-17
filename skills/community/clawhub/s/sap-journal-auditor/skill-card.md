## Description:

Audits SAP FI/CO journal exports to detect duplicates, anomalies, cost center mismatches, approval bypass, intercompany issues, and unusual user activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dda-oo](https://clawhub.ai/user/dda-oo)

### License/Terms of Use:

CC-BY-4.0

## Use Case:

Controllers, internal auditors, finance teams, and audit-prep teams use this skill to review exported SAP FI/CO journal data for duplicate postings, period-end anomalies, approval bypass indicators, intercompany issues, and unusual user activity. It produces review-ready findings that still require human audit judgment before corrective action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive SAP financial exports and writes generated memo and CSV files as persistent outputs.

Mitigation: Run it in a sandboxed workspace with limited filesystem access and review storage, retention, and sharing of generated files before use.

Risk: The skill asks for more execution authority than its normal audit workflow appears to require.

Mitigation: Remove shell permission where possible and grant only the file access needed for the uploaded export and generated outputs.

Risk: Generated CSV files may preserve spreadsheet formulas from untrusted source data until formula neutralization is fixed.

Mitigation: Avoid opening generated CSVs in spreadsheet software from untrusted inputs, or neutralize formula-leading characters before review.

Risk: Spreadsheet parsing may be exposed to large or malformed files.

Mitigation: Keep dependencies updated and apply file-size, row-count, and execution-time limits for CSV and Excel processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dda-oo/skills/sap-journal-auditor)
- [ClawHub publisher profile](https://clawhub.ai/user/dda-oo)
- [Artifact README](artifact/README.md)
- [Artifact security policy](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV, Files, Guidance]

**Output Format:** [Chat summary plus Markdown audit memo and CSV flagged-entry export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports English or German output, optional fiscal-period filtering, and configurable duplicate-amount threshold.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
