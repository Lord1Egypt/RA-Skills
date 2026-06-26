## Description: <br>
筛选测试用例Excel文件，提取P0/P1优先级用例，删除项目/产品列，重新编号并保持原格式 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yontlly](https://clawhub.ai/user/yontlly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and test teams use this skill to turn Excel test-case workbooks into focused P0/P1 execution sets while preserving workbook formatting and renumbering cases per sheet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes transformed Excel workbooks and may overwrite important files if the same path is reused. <br>
Mitigation: Run the skill on copies or choose a distinct output filename, then review the generated workbook before using it downstream. <br>
Risk: Auxiliary scripts include hard-coded local Windows paths that may not match the user's environment. <br>
Mitigation: Use the main command-line or Python entry point for normal processing, and edit hard-coded paths before running auxiliary scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yontlly/testcase-filter) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Analysis, Shell commands, Code] <br>
**Output Format:** [Processed .xlsx workbook plus text status and summary output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Filters sheets to P0/P1 rows, removes project/product columns, splits merged cells, preserves formatting where supported, and renumbers cases from TC001 per sheet.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
