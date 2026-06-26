## Description: <br>
Use this skill when a spreadsheet file is the primary input or output, including reading, creating, editing, formatting, analyzing, or converting .xlsx, .xlsm, .csv, and .tsv files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinfeihaaaaaaaaaaa](https://clawhub.ai/user/yinfeihaaaaaaaaaaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and spreadsheet-focused agents use this skill to inspect, create, modify, and verify spreadsheet deliverables while preserving formulas, formatting, and financial-model conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The formula recalculation helper can run local LibreOffice, modify workbooks, and leave a persistent macro in the user's LibreOffice profile. <br>
Mitigation: Review before installing, use copies of important spreadsheets, and prefer versions that ask before profile changes, use a temporary LibreOffice profile, clean up the macro, and remove shell=True. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinfeihaaaaaaaaaaa/xlsx-localized) <br>
- [LibreOffice download](https://www.libreoffice.org/download/download-libreoffice/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify spreadsheet files when an agent follows the workflow. Formula recalculation depends on a local LibreOffice installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
