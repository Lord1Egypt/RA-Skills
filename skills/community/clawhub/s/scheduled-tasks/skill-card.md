## Description: <br>
Create and manage OpenClaw scheduled tasks for reminders, periodic notifications, and automated workflows using OpenClaw Cron API or system crontab. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chowlee-cc](https://clawhub.ai/user/chowlee-cc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to create, manage, test, and troubleshoot scheduled OpenClaw agent tasks, reminders, Feishu notifications, and shell-script cron workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Misconfigured scheduled tasks can send recurring messages to unintended Feishu recipients. <br>
Mitigation: Verify the schedule, account, recipient ID, and message content, then test with a safe target before enabling recurring delivery. <br>
Risk: Old scheduled jobs can continue running after they are no longer needed. <br>
Mitigation: Periodically list, disable, or remove OpenClaw Cron and system crontab jobs that are no longer required. <br>


## Reference(s): <br>
- [Scheduled Tasks Skill Page](https://clawhub.ai/chowlee-cc/scheduled-tasks) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OpenClaw Cron commands, crontab entries, troubleshooting checks, and shell script templates.] <br>

## Skill Version(s): <br>
2.1.7 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
