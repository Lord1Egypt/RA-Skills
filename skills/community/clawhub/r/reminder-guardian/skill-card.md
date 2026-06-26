## Description: <br>
Helps users remember things by keeping a list of reminders, creating scheduled-job blueprints, and tracking which reminders are done. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a-suraj-bhatti](https://clawhub.ai/user/a-suraj-bhatti) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to log reminder requests, generate human-reviewed OpenClaw cron blueprints, and keep reminder status records current. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script computes the time-helper path incorrectly and may execute Python code outside the reviewed skill package. <br>
Mitigation: Review or fix the time-helper path before installing or running the skill. <br>
Risk: Reminder text and notes are stored in a local reminder log and may contain sensitive information. <br>
Mitigation: Avoid putting secrets in reminder text and remove reminder log entries when they are no longer needed. <br>
Risk: Cron blueprints can create scheduled jobs if copied into OpenClaw without review. <br>
Mitigation: Inspect the generated cron blueprint before adding it and remove scheduled jobs when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a-suraj-bhatti/reminder-guardian) <br>
- [Skill documentation](artifact/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style instructions with shell commands and JSON cron blueprints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local reminder log and prints cron blueprints that must be reviewed and added manually with openclaw cron add.] <br>

## Skill Version(s): <br>
0.1.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
