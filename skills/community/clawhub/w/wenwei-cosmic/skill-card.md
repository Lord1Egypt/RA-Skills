## Description: <br>
基于 COSMIC 标准的工作量拆分工作流。将需求文档自动拆解为功能点与子过程明细（E/R/W/X 数据移动），生成拆解表格与 CSV 文件。当用户要求进行 COSMIC 拆分、功能点分析、COSMIC 工作量拆解时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wed840313](https://clawhub.ai/user/wed840313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and delivery teams use this skill to decompose requirements documents into COSMIC function points and E/R/W/X data-movement subprocesses. It supports review of Markdown breakdowns and CSV export for downstream estimation work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask the agent to run a simple local shell command for output validation or CSV conversion. <br>
Mitigation: Review the prompted command before execution, especially in restricted environments. <br>
Risk: COSMIC decomposition results may be incomplete or misleading if the input requirements are ambiguous or insufficient. <br>
Mitigation: Use the built-in review and confirmation steps before relying on the generated Markdown or CSV outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wed840313/wenwei-cosmic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and CSV files, with concise progress and review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask the agent to run a local Python conversion command after the Markdown breakdown has been reviewed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
