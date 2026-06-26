## Description: <br>
Schedule and manage OpenClaw tasks from natural language with timezone-aware cron lifecycle commands, logs, and failure alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariusfit](https://clawhub.ai/user/mariusfit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use Smart Cron to schedule unattended OpenClaw tasks such as briefings, monitoring, reports, and cleanup without writing cron syntax. It provides lifecycle commands, next-run previews, local logs, and optional failure alerts for recurring jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended recurring execution can repeatedly run an incorrect, stale, or overly broad OpenClaw task. <br>
Mitigation: Review each scheduled task before enabling it, use pause or remove commands for jobs that are no longer needed, and periodically audit the job list. <br>
Risk: Task names, prompts, logs, or alert messages may expose sensitive operational details through local storage or messaging channels. <br>
Mitigation: Avoid putting secrets in scheduled task text, confirm alert channels are private, and review local logs and retention settings. <br>


## Reference(s): <br>
- [Smart Cron ClawHub page](https://clawhub.ai/mariusfit/smart-cron) <br>
- [Smart Cron source repository](https://github.com/mariusfit/smart-cron) <br>
- [Smart Cron issues](https://github.com/mariusfit/smart-cron/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces cron lifecycle commands, schedule descriptions, local configuration guidance, and log inspection guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
