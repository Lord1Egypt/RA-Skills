## Description: <br>
Five-phase token audit and optimization framework for OpenClaw agents: discover, prioritize, optimize, validate, and monitor token usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youxiyin](https://clawhub.ai/user/youxiyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of OpenClaw agents use this skill to audit scheduled tasks, prompts, context loading, model routing, and tool profiles, then produce practical token-saving recommendations and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose or directly change prompts, model routing, cron schedules, provider settings, and tool profiles. <br>
Mitigation: Run it in read-only or proposal mode first, require a diff and rollback plan before applying moderate or high-risk changes, and approve configuration edits explicitly. <br>
Risk: Audit reports may include local filenames, task names, prompt text, and configuration details. <br>
Mitigation: Review generated reports before sharing them outside the deployment context. <br>
Risk: Some configuration changes require a gateway restart or can affect scheduled-agent behavior. <br>
Mitigation: Validate JSON configuration, confirm restart requirements, and test cron or heartbeat behavior after edits. <br>


## Reference(s): <br>
- [Wave Token Saver on ClawHub](https://clawhub.ai/youxiyin/wave-token-saver) <br>
- [OpenClaw Cron Jobs](https://docs.openclaw.ai/automation/cron.md) <br>
- [OpenClaw Standing Orders](https://docs.openclaw.ai/automation/standing-orders.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with tables, proposed changes, JSON snippets, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Full executions write token-audit-report-YYYY-MM-DD.md; recommendations can include before-and-after comparisons, estimated savings, deferred items, and next steps.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
