## Description: <br>
自动化操作 vue-element-admin 管理系统的综合 Table 页面，包括登录、遍历数据、修改记录并导出到 Excel。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mingj](https://clawhub.ai/user/mingj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators can use this skill to automate a Vue admin demo table workflow: log in, inspect rows, update importance values, and export captured table data to a dated Excel file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow edits table records in the target admin interface. <br>
Mitigation: Use scoped credentials and require explicit confirmation before saving edits, especially on any real admin system. <br>
Risk: The workflow writes a dated Excel file to the Desktop and may overwrite or conflict with an existing file. <br>
Mitigation: Choose and confirm the output path before execution, and check whether the file already exists before writing. <br>
Risk: The skill includes demo login credentials and browser actions for a specific public Vue admin demo. <br>
Mitigation: Install and run it only when that specific demo automation is intended; replace credentials and selectors with approved values for any private environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mingj/vue-table-operation) <br>
- [vue-element-admin demo](https://panjiachen.github.io/vue-element-admin/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown instructions with Python and browser automation snippets; generated Excel workbook] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a dated .xlsx file on the Desktop when followed by an agent with browser automation and openpyxl access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
