## Description: <br>
StartClaw-Optimizer helps agents route tasks by complexity, compact long context, schedule retries, govern browser concurrency, and monitor cost-related workflow metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[idanmann10](https://clawhub.ai/user/idanmann10) <br>

### License/Terms of Use: <br>
StartClaw Internal Use License <br>


## Use Case: <br>
Developers and agent operators use this skill to reduce token and cost growth by routing simple tasks to lighter models, compacting large contexts, wrapping automated tasks in scheduler retries, and monitoring model and budget usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill claims broad agent-control behavior for model routing, context handling, scheduling, and browser workflow control. <br>
Mitigation: Install it only when that broad optimization role is intended, and review routing, compaction, scheduler, and browser-governor behavior before relying on it. <br>
Risk: The release handles session context and may log session identifiers or detected context themes. <br>
Mitigation: Avoid logging raw session identifiers or sensitive context themes, and review logging configuration before use with private work. <br>
Risk: The installation example uses an unpinned package path. <br>
Mitigation: Pin and verify the npm package version before installing or deploying the skill. <br>
Risk: Scheduler retries can repeat task execution. <br>
Mitigation: Use scheduler retries only for tasks where repeated execution is safe or idempotent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/idanmann10/startclaw-optimizer) <br>
- [Skill overview](SKILL.md) <br>
- [Context compaction README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include model-routing decisions, cost estimates, compaction recommendations, retry behavior, and monitoring commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
