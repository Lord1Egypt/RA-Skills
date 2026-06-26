## Description: <br>
Schedule and run recurring tasks on Linux/Unix systems. Use when user wants to set up cron jobs, scheduled backups, periodic data sync, automated reports, or any recurring task automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create, inspect, enable, disable, and remove recurring cron-based jobs for backups, syncs, reports, monitoring, and similar automation on Linux or Unix systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist arbitrary cron commands. <br>
Mitigation: Review each scheduled command before adding it and avoid sensitive or destructive commands with this version. <br>
Risk: Crontab handling may delete unrelated entries or fail to remove scheduled jobs cleanly. <br>
Mitigation: Back up the current crontab before use and verify cron entries manually after add, remove, enable, or disable operations. <br>
Risk: Log file access and task metadata are controlled by user-provided paths and values. <br>
Mitigation: Use scheduler-owned log paths, avoid sensitive files, and validate cron, command, and log values before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/schedule-task) <br>
- [Publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify the user's crontab and store task metadata under the user's configuration directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
