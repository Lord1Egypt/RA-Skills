## Description: <br>
Unified Task Orchestration Hub v2.3 integrates heartbeat, cron, subagent, and task-management workflows for task identification, standardized setup, execution tracking, channel binding, deadlock prevention, and aggregation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloechien511-cloud](https://clawhub.ai/user/chloechien511-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to classify requests as cron, heartbeat, subagent, task-record, or immediate work, then generate plans, setup steps, templates, and commands for OpenClaw task orchestration. It is especially relevant for recurring reminders, monitoring workflows, multi-agent task breakdowns, and execution tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring cron or heartbeat automations may send messages or create scheduled tasks with unintended recipients, accounts, channels, or timing. <br>
Mitigation: Replace every recipient ID, accountId, channel, agentId, and timezone with environment-specific values and require confirmation before sending messages or creating recurring tasks. <br>
Risk: Monitoring workflows can create noisy or inappropriate alerts if inbox, calendar, urgency, and cooldown rules are underspecified. <br>
Mitigation: Define exact urgency rules, quiet hours, cooldowns, and escalation conditions before enabling monitoring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chloechien511-cloud/task-orchestrator-cron-heartbeat-subagent) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact quick start](artifact/QUICKSTART.md) <br>
- [OpenClaw cron jobs documentation](https://docs.openclaw.ai/automation/cron-jobs) <br>
- [OpenClaw website](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, task templates, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw and user-specific agentId, accountId, channel, recipient, timezone, and monitoring-rule values before automation is enabled.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence; artifact frontmatter version: 2.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
