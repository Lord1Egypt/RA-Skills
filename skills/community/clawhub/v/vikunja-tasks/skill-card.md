## Description: <br>
Manage tasks and projects on a self-hosted Vikunja instance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickian](https://clawhub.ai/user/nickian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users use this skill to manage task lists, projects, due dates, completions, and notifications on a self-hosted Vikunja instance through its REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Specially crafted search or filter text may run local commands through the URL-encoding flaw reported by the security scan. <br>
Mitigation: Patch scripts/vikunja.sh so user text is passed to Python as an argument or environment variable before installing or running the skill. <br>
Risk: The skill uses a Vikunja API token to create, complete, and read tasks and projects. <br>
Mitigation: Use a limited Vikunja token, store it as a secret, and confirm create, complete, and project-changing actions before execution. <br>
Risk: Recurring due-date checks and Telegram delivery may disclose task information outside the Vikunja instance. <br>
Mitigation: Enable the cron and Telegram notification workflow only when recurring checks and external task notifications are intended. <br>


## Reference(s): <br>
- [Vikunja filter syntax](https://vikunja.io/docs/filters) <br>
- [ClawHub skill page](https://clawhub.ai/nickian/vikunja-tasks) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown and plain text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May issue REST API requests to a configured Vikunja instance when commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
