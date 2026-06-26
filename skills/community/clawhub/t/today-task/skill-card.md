## Description: <br>
通用任务结果推送器，当任务完成后将结果推送到负一屏。使用统一的标准数据格式，支持各种类型的任务结果推送。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ganhaiyang3](https://clawhub.ai/user/ganhaiyang3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill to format completed task results as JSON, push the resulting Markdown content and task metadata to a configured HiBoard endpoint, and report push or update-check status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authorization codes, task content, and task metadata are sent to the configured endpoint. <br>
Mitigation: Install only when that data flow is acceptable, use a trusted endpoint, and configure the authorization code through OpenClaw configuration instead of chat. <br>
Risk: Local logs and push records may retain task-related data by default. <br>
Mitigation: Review local records, disable record saving when appropriate, and avoid pushing highly sensitive task content. <br>
Risk: The skill includes default-enabled update-check behavior. <br>
Mitigation: Review update-check settings and disable or constrain them if network calls to ClawHub are not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ganhaiyang3/today-task) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON task files and Markdown or text status messages with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send task content, metadata, and an authorization code to the configured endpoint; may store local logs and push records.] <br>

## Skill Version(s): <br>
1.0.17 (source: server release metadata and artifact version.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
