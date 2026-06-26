## Description: <br>
Track and log AI API usage across providers, calculate costs, and generate daily, weekly, or monthly reports filtered by model and task type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[punkaze](https://clawhub.ai/user/punkaze) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and teams use this skill to record AI API calls, estimate provider costs, and review usage by day, week, month, model, or task type. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local usage logs can expose provider, model, token-count, and task-type history if retained too long or shared unintentionally. <br>
Mitigation: Avoid sensitive task labels, restrict access to the log file, and periodically delete or rotate usage-logs/api-cells.jsonl when retention matters. <br>
Risk: Telegram usage reports may disclose usage and cost details to chat participants. <br>
Mitigation: Use Telegram reporting only in trusted chats and review report content before sharing it more broadly. <br>


## Reference(s): <br>
- [Usage Tracker on ClawHub](https://clawhub.ai/punkaze/usage-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style usage and cost reports with tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Logs usage records to usage-logs/api-cells.jsonl; reports can be filtered by period, model, and task type.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
