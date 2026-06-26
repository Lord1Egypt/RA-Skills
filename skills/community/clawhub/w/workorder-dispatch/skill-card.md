## Description: <br>
工单分派与SLA监控技能，基于 Excel 台账自动分派报修工单、跟踪处理进度，并对 SLA 超时工单进行升级提醒。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations and facilities teams use this skill to create, dispatch, monitor, update, and escalate maintenance work orders from an Excel-based service ledger. It supports WeCom-triggered intake, hourly SLA checks, status summaries, completion confirmation, and feedback capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to read and modify a live local Excel work-order ledger. <br>
Mitigation: Run it only where the agent is authorized to access the named workbook, move the workbook path into controlled configuration, and add backups and audit logging before enabling writes. <br>
Risk: Work-order details may include personal, location, cost, or incident information that is broadcast through WeCom notifications. <br>
Mitigation: Restrict notification recipients, redact sensitive details where possible, and control who can create, query, or update work orders. <br>
Risk: The feedback flow writes rating and comment fields beyond the documented 13-column workbook schema. <br>
Mitigation: Fix and validate the workbook feedback schema before enabling feedback writes. <br>
Risk: Webhook and workbook settings are shown as inline configuration values. <br>
Mitigation: Store webhook URLs and workbook paths in controlled configuration or secret storage rather than hard-coding them in skill text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/perrykono-debug/workorder-dispatch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown, JSON examples, Python code snippets, and notification text templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include work-order summaries, dispatch decisions, SLA timeout lists, WeCom notification payload text, configuration examples, and workbook update guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
