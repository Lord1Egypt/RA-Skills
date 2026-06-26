## Description: <br>
读取 Excel 文件，按照指定列分组，并将每个分组导出为按分组字段命名的新 Excel 文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoming](https://clawhub.ai/user/guoming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations users and developers use this skill to split a self-operated delivery strategy Excel workbook into grouped zone-configuration files. It is intended for local spreadsheet processing where grouping columns and an output folder are supplied by the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input spreadsheets or grouping columns may be incorrect, producing incomplete or misleading exported zone files. <br>
Mitigation: Run the script on a copy or known-good source spreadsheet and inspect generated files before operational use. <br>
Risk: Generated files can overwrite existing files in the selected output folder when group-derived filenames collide. <br>
Mitigation: Use a fresh output folder for each run and review filenames before relying on the export results. <br>
Risk: The script depends on pandas and Excel-reading dependencies from the local Python environment. <br>
Mitigation: Install pandas-related dependencies from trusted package sources and run the tool in an environment appropriate for local spreadsheet processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guoming/self-operated-delivery-strategy-excel-group-export) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Excel files and Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports one .xlsx file per group, retaining only the generated zone columns: 分区名称, 国家二字码, 城市, 开始邮编, 结束邮编.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
