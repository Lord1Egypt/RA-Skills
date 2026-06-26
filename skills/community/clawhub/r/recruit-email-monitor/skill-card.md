## Description: <br>
Monitors configured mailboxes for recruitment-related emails, records matching messages in an Excel workbook, and sends Feishu alerts and daily briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haoxianniu528-bit](https://clawhub.ai/user/haoxianniu528-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers and recruiting workflow operators use this skill to monitor mailbox accounts for application updates, interview notices, assessments, offers, and other recruiting messages. It helps an agent keep a structured tracker and notify the user when new or pending recruiting emails need attention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes real-looking mailbox authorization codes and a fixed Feishu recipient. <br>
Mitigation: Remove the embedded values, rotate any exposed mailbox authorization codes, and configure a verified recipient before running the scripts. <br>
Risk: The scripts use fixed local storage paths for the Excel tracker and daily briefing. <br>
Mitigation: Change the paths to an approved writable location and confirm the stored email fields match the user's privacy expectations. <br>
Risk: Imported cron jobs would repeatedly access configured mailboxes and send notifications. <br>
Mitigation: Run the scripts manually after configuration review, then import the cron jobs only if recurring monitoring is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haoxianniu528-bit/recruit-email-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/haoxianniu528-bit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown documentation with inline shell commands, Python configuration examples, Excel workbook output, and text briefing output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local mailbox credentials, Feishu recipient configuration, writable file paths, and optional recurring cron execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
