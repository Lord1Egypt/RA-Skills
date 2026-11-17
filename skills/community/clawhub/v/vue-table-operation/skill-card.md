## Description:

自动化操作 vue-element-admin 管理系统的综合 Table 页面，包括登录、遍历数据、修改记录并导出到 Excel。适用于需要批量处理 Table 数据的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingj](https://clawhub.ai/user/mingj)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to automate a vue-element-admin demo table workflow: sign in, visit the comprehensive Table page, inspect rows, update importance ratings, and export table details to Excel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow uses embedded demo credentials.

Mitigation: Use the credentials only for the documented vue-element-admin demo and confirm the target site before logging in.

Risk: The workflow edits table records in the web app.

Mitigation: Review the target record and intended importance value before saving changes.

Risk: The workflow writes a dated Excel file to the desktop.

Mitigation: Confirm or adjust the output path before running the export steps.

## Reference(s):

- [vue-element-admin demo](https://panjiachen.github.io/vue-element-admin/)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with inline Python and browser automation snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces procedural automation steps and Excel-writing examples for a browser-driven workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
