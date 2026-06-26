## Description: <br>
Compares SOP and BOM Excel files, including one SOP against multiple merged BOM files, and generates an independent review report with side-by-side differences, SOP-only materials, BOM-only materials, red difference markings, and yellow duplicate-material markings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2656255594](https://clawhub.ai/user/2656255594) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Manufacturing, quality, and engineering users can use this skill to compare SOP spreadsheets with one or more BOM spreadsheets and produce an Excel report that highlights mismatched material names, positions, quantities, duplicates, and materials present in only one source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local script reads user-provided SOP and BOM spreadsheets and writes an Excel report. <br>
Mitigation: Run it only on spreadsheets you are comfortable processing locally and avoid elevated privileges. <br>
Risk: Report cleanup may remove older files in the selected output directory that match the 校对报告 .xlsx naming pattern. <br>
Mitigation: Keep important reports outside the selected output directory or rename them before running cleanup behavior. <br>
Risk: Manual cleanup commands can delete temporary files matching SOP/BOM extraction patterns. <br>
Mitigation: Review cleanup commands before running them manually and restrict them to the intended temporary directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2656255594/sop-bom-report) <br>
- [Publisher profile](https://clawhub.ai/user/2656255594) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples for producing an Excel .xlsx comparison report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated report contains three worksheets or sections for differing materials, SOP-only materials, and BOM-only materials, with color highlighting for differences and duplicates.] <br>

## Skill Version(s): <br>
1.4.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
