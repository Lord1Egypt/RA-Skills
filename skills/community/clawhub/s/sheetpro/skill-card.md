## Description: <br>
Creates, edits, analyzes, converts, and verifies spreadsheet deliverables such as .xlsx, .xlsm, .csv, and .tsv files using Python spreadsheet libraries and LibreOffice recalculation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Developers and agents use this skill when a spreadsheet file is the primary input or deliverable, including workbook creation, formula authoring, formatting, charting, tabular data cleanup, conversion, and QA. It is intended for spreadsheet outputs rather than Word documents, HTML reports, standalone scripts, database pipelines, or Google Sheets integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports under-disclosed native LibreOffice shimming. <br>
Mitigation: Run the skill in a disposable or sandboxed environment and review any native helper compilation or LD_PRELOAD use before execution. <br>
Risk: The security review reports persistent LibreOffice macro changes. <br>
Mitigation: Use an isolated LibreOffice profile for execution, keep workbook backups, and remove or reset the profile after use. <br>
Risk: The security review reports off-scope Word and PowerPoint document handling. <br>
Mitigation: Restrict use to expected spreadsheet workflows and avoid untrusted Office documents until the off-scope behavior is removed or clearly controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fslong520/sheetpro) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Spreadsheet files with Markdown guidance, Python code snippets, shell commands, and JSON validation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke LibreOffice formula recalculation and Office validation helpers before delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
