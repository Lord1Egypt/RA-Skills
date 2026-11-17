## Description:

Automates local office workflows for documents, spreadsheets, presentations, and PDFs, including generation, polishing, review, cleaning, analysis, charting, conversion, extraction, merge, and split tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyuanhua](https://clawhub.ai/user/zyuanhua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and office users use this skill to automate local processing of office files, including document creation, contract review, spreadsheet cleanup and analysis, presentation creation, and PDF conversion or extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad filesystem access can expose sensitive local office documents.

Mitigation: Run the skill in a constrained workspace and only grant access to directories needed for the current task.

Risk: Malformed PDFs, spreadsheets, or images may cause denial of service or increase parser exploit risk.

Mitigation: Avoid untrusted files, update parsing dependencies before deployment, and add file type and size limits.

Risk: Generated file output and overwrite behavior is not fully documented.

Mitigation: Review output paths before use and require explicit destination handling for workflows that write files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zyuanhua/skills/wps-office-automation-skill)

## Skill Output:

**Output Type(s):** [text, files, structured data]

**Output Format:** [JSON responses with text, structured fields, and Base64-encoded office files when a file is produced.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return generated DOCX, XLSX, PPTX, or PDF artifacts, extracted text, analysis results, and status messages.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
