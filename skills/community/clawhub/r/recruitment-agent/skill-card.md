## Description: <br>
Recruitment Agent helps manage recruiting workflows across Boss Zhipin and Feishu/Lark, including message review, candidate database updates, decision records, and interview scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billzhuang6569](https://clawhub.ai/user/billzhuang6569) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters and hiring teams use this skill to triage Boss Zhipin conversations, save or update candidate records in Feishu/Lark Base, record hiring decisions, and coordinate interview scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can monitor candidate messages, store sensitive hiring data, modify records, send outreach, and create calendar events. <br>
Mitigation: Require explicit user confirmation before outreach, calendar creation, database writes, or recurring polling tasks. <br>
Risk: Candidate records and freeform summaries may capture sensitive personal or hiring data. <br>
Mitigation: Limit stored fields to necessary recruiting information and avoid copying sensitive attributes into freeform summaries. <br>
Risk: Recurring polling can continue monitoring candidate conversations after it is no longer needed. <br>
Mitigation: Use visible stop conditions and delete the polling task after the interview is scheduled or the workflow ends. <br>


## Reference(s): <br>
- [Recruitment Agent ClawHub Page](https://clawhub.ai/billzhuang6569/recruitment-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/billzhuang6569) <br>
- [Save Candidate Workflow](references/workflow-2-save-candidate.md) <br>
- [Decision Record Workflow](references/workflow-3-decision-record.md) <br>
- [Update Candidate Workflow](references/workflow-4-update-candidate.md) <br>
- [Schedule Interview Workflow](references/workflow-schedule-interview.md) <br>
- [Calendar Utility](references/util-check-calendar.md) <br>
- [Feishu Message Utility](references/util-send-feishu-message.md) <br>
- [Heartbeat Task](references/heartbeat_task.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured recruiting summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute recruiting workflow steps that read messages, update records, send outreach, create calendar events, or create recurring polling tasks.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
