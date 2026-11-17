## Description:

WPS Office workflow for Chinese users: create, edit, review, convert, and troubleshoot Writer, Spreadsheets, and Presentation documents in .docx, .xlsx, .pptx, and WPS native formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate and guide Chinese WPS Office document workflows, including format conversion, Chinese document generation, spreadsheet cleanup, delivery inspection, and compatibility troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local scripts against user-selected Office documents, which may contain sensitive business or personal data.

Mitigation: Review document contents before conversion or cleanup, avoid exposing real sensitive data in examples, and run the scripts only on files the user intentionally provides.

Risk: The Python helper scripts depend on local packages and office conversion tools such as python-docx, openpyxl, and LibreOffice.

Mitigation: Use a virtual environment, prefer pinned dependencies, and confirm required binaries are installed before relying on generated or converted files.

Risk: Spreadsheet cleanup and document conversion can change files or produce delivery artifacts that need review.

Mitigation: Keep source copies, use generated output files or backups where available, and inspect converted documents before delivery.

## Reference(s):

- [WPS Reference](references/wps-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/jvy/skills/wps)
- [LibreOffice Downloads](https://www.libreoffice.org/download/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and optional generated Office files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local .docx, .xlsx, .pptx, .pdf, and backup files when the bundled scripts are run on user-selected documents.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
