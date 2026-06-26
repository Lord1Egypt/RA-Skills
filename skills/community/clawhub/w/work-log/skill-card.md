## Description: <br>
Automated work log management with daily and weekly report generation for recording tasks, tracking progress, setting reminders, and marking task completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwl52](https://clawhub.ai/user/wwl52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and individual contributors use this skill to maintain a local plaintext work log, track task progress, receive reminders for incomplete work, and generate daily or weekly summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Work log entries are stored locally as plaintext and may contain sensitive workplace details. <br>
Mitigation: Avoid logging secrets, credentials, regulated data, or customer-confidential information unless local storage on the device is acceptable. <br>
Risk: Recurring progress reminders can surface task names and status during working hours. <br>
Mitigation: Use explicit completion or deletion commands to close or remove tasks and keep reminder content nonsensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wwl52/work-log) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown tables and text summaries, plus local JSON log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores logs locally at ~/.workbuddy/work-log/logs.json and may schedule recurring progress reminders.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata; artifact frontmatter reports 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
