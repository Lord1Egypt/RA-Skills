## Description: <br>
Automates WeCom Smart Sheet workflows by helping agents write records, send group notifications, maintain a local deadline tracker, and prepare reminders for expense, task, and video-production workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason918262](https://clawhub.ai/user/jason918262) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operations teams use this skill to turn natural-language requests into WeCom Smart Sheet record creation, matching group notifications, local deadline tracking, and reminders for expenses, tasks, and video production workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write business records to WeCom Smart Sheets and send WeCom group notifications. <br>
Mitigation: Use least-privilege webhook and bot keys, and confirm each live write and notification destination before execution. <br>
Risk: The local deadline tracker may store business, personnel, financial, or schedule details. <br>
Mitigation: Avoid storing unnecessary sensitive details, restrict access to the tracker file, and periodically review or delete old records. <br>
Risk: Scheduled reminders and daily checks can continue sending notifications after business context changes. <br>
Mitigation: Review active reminders and tracker records regularly, and remove obsolete schedules or records. <br>
Risk: Incorrect user IDs, field formats, or table-to-group mapping can cause failed writes or messages sent to the wrong group. <br>
Mitigation: Validate WeCom user IDs and field formats before posting, and keep each table mapped only to its corresponding group bot. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jason918262/wecom-smartsheet) <br>
- [Publisher profile](https://clawhub.ai/user/jason918262) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [wecom_smartsheet.py](artifact/references/wecom_smartsheet.py) <br>
- [wecom_daily_check.py](artifact/references/wecom_daily_check.py) <br>
- [wecom_deadline_tracker.json](artifact/wecom_deadline_tracker.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads, shell commands, and Python helper references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce WeCom webhook payloads, group-message content, local tracker entries, and reminder setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
