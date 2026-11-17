## Description:

Helps agents create, read, edit, analyze, convert, format, and verify .xlsx, .xlsm, .csv, and .tsv spreadsheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinfeihaaaaaaaaaaa](https://clawhub.ai/user/yinfeihaaaaaaaaaaa)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to build, modify, inspect, and QA spreadsheet deliverables, especially Excel workbooks with formulas, formatting, financial-model conventions, and LibreOffice recalculation checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The formula recalculation helper can persistently modify or overwrite a user's LibreOffice macro module.

Mitigation: Run it only after review, preferably with a temporary LibreOffice profile, a skill-specific macro name, and explicit user consent for profile changes.

Risk: Spreadsheet recalculation can overwrite important workbook files during processing.

Mitigation: Use copies or backups of important workbooks until the helper adds file-type allowlisting and safer overwrite controls.

## Reference(s):

- [LibreOffice download](https://www.libreoffice.org/download/download-libreoffice/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples, plus spreadsheet files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use pandas, openpyxl, and LibreOffice for formula recalculation and spreadsheet error checks.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
