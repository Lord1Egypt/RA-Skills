## Description: <br>
通过 zentao 命令行工具查询和操作禅道（ZenTao）数据，覆盖项目集、产品、项目、执行、需求、Bug、任务、测试用例、测试单、产品计划、版本、发布、反馈、工单、应用、用户、附件等模块的增删改查及状态流转。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catouse](https://clawhub.ai/user/catouse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, project managers, QA engineers, and support teams use this skill to query and operate ZenTao project-management records through the zentao CLI. It helps agents list, inspect, create, update, delete, and transition ZenTao objects when the user explicitly asks for ZenTao work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, delete, and transition ZenTao project-management data. <br>
Mitigation: Require clear user confirmation before create, update, delete, user, file, or status-change operations. <br>
Risk: The skill may activate on generic project-management requests. <br>
Mitigation: Keep usage tied to explicit ZenTao or zentao-cli requests before running commands. <br>
Risk: The workflow depends on an external globally installed zentao-cli package. <br>
Mitigation: Review the external package before global installation and prefer the user's approved package manager. <br>
Risk: ZenTao credentials and tokens are sensitive. <br>
Mitigation: Do not collect credentials in chat or read local credential files or environment variables; let the CLI handle authentication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/catouse/zentao-cli) <br>
- [Publisher profile](https://clawhub.ai/user/catouse) <br>
- [zentao-cli repository metadata](https://github.com/easysoft/zentao-cli.git) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI output is Markdown by default or JSON when --format=json is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external zentao CLI and a user-authorized ZenTao account; write operations should be confirmed before execution.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
