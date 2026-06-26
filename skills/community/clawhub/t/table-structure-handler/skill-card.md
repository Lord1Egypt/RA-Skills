## Description: <br>
Formats Excel table-structure workbooks by deleting the title row, adding standardized F-N headers, inserting default metadata, applying table styles, and saving a processed copy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cztzb](https://clawhub.ai/user/cztzb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data documentation teams use this skill to process uploaded Chinese table-structure Excel workbooks into a standardized table format while preserving the original workbook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes uploaded Excel workbooks and can select the latest .xlsx file or use fuzzy filename matching, which may transform the wrong workbook if filenames are ambiguous. <br>
Mitigation: Use simple, exact .xlsx filenames when invoking the skill and review the processed workbook before relying on it. <br>
Risk: Spreadsheet transformations may not match expectations for unusual workbook structures, merged cells, or nonstandard table layouts. <br>
Mitigation: Keep the original workbook, inspect the generated _processed.xlsx output, and rerun with corrected input if the resulting table structure is not acceptable. <br>


## Reference(s): <br>
- [Housing Provident Fund Basic Data Standard (Draft for Approval) 1001](artifact/references/住房公积金基础数据标准（报批稿）1001.md) <br>
- [ClawHub skill page](https://clawhub.ai/cztzb/table-structure-handler) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Guidance] <br>
**Output Format:** [Processed .xlsx workbook plus console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a non-overwriting processed workbook, typically <filename>_processed.xlsx, to /workspace/skills_output/.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
