## Description: <br>
schedule-reminder helps agents create scheduled reminders, maintain a local backup reminder ledger, and send daily schedule briefs through OpenClaw cron and messaging tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayting511](https://clawhub.ai/user/jayting511) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create one-time reminders from explicit requests or detected schedule details, send reminders over configured messaging channels, and receive a daily schedule preview. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs background reminder checks through OpenClaw cron and a system-level fallback scheduler. <br>
Mitigation: Install only when a background reminder service is expected, review the configured user ID, account ID, channel, and timezone, and remove crontab or LaunchAgent entries during uninstall if needed. <br>
Risk: Reminder text and daily brief content may be stored locally and sent through the configured messaging channel. <br>
Mitigation: Avoid placing secrets or sensitive content in reminder titles, messages, or advisor text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jayting511/schedule-reminder) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates reminder records, scheduled jobs, local backup files, and messaging output through the configured OpenClaw tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
