## Description: <br>
Local team scheduling skill that uses Python and SQLite to manage shared schedules, detect conflicts, send email summaries, and send DingTalk reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renhao12356578](https://clawhub.ai/user/renhao12356578) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams use this skill to add, update, search, delete, and review shared schedule entries through natural-language requests. It is also used to configure scheduled email summaries and DingTalk reminders for upcoming events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run background reminder and email-summary jobs that send schedule details to chat or email. <br>
Mitigation: Before enabling cron, DingTalk, or email summaries, confirm the intended recipients, visibility of schedule entries, and how to disable the jobs. <br>
Risk: Shared team schedules may contain sensitive meeting notes, locations, or timing details. <br>
Mitigation: Exclude sensitive notes from reminders and confirm who can view or receive schedule entries before using shared or group delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/renhao12356578/smartschedule) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce schedule summaries, conflict-resolution options, reminder setup instructions, and command invocations for local Python scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
