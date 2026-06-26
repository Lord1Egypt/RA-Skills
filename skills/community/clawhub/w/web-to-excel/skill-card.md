## Description: <br>
Extracts structured data from webpages and helps fill user-specified ranges in Excel workbooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oreosofat](https://clawhub.ai/user/oreosofat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to extract tabular or parameter-style data from webpages and populate user-selected Excel files, sheets, rows, and columns. It is intended for workflows where the user provides the URL, workbook path, sheet name, range, and field mapping at runtime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify and save the selected Excel workbook. <br>
Mitigation: Use a copy of important spreadsheets and verify the workbook path, sheet name, row range, and field-to-column mapping before saving changes. <br>
Risk: The skill can use a local browser debugging endpoint to inspect webpage content. <br>
Mitigation: Use it only with intended URLs and browser tabs, and close unrelated sensitive tabs before connecting to the debugging endpoint. <br>
Risk: The skill can install Python packages at runtime. <br>
Mitigation: Preinstall and pin required dependencies in a controlled environment where possible. <br>


## Reference(s): <br>
- [Field Mapping Reference](references/field-mapping.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/oreosofat/web-to-excel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline Python and shell command examples, plus workbook update summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce proposed field mappings, confirmation prompts, Python execution steps, and a summary of updated rows and columns.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
