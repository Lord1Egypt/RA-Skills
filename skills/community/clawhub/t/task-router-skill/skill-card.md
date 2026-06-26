## Description: <br>
Distributed task queue and agent coordinator for OpenClaw multi-agent systems that routes tasks by capability, tracks lifecycle, coordinates async handoffs, rebalances loads, and manages dead letters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[capt-marbles](https://clawhub.ai/user/capt-marbles) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multi-agent OpenClaw work through capability-based task routing, task lifecycle tracking, async handoffs, workload rebalancing, and dead-letter handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local task state and automated routing can expose sensitive payloads or route work to inappropriate agents. <br>
Mitigation: Register only trusted agents, scope agent capabilities carefully, and avoid putting secrets in task payloads or result files. <br>
Risk: Heartbeat automation can reassign, retry, or spawn work without immediate human review. <br>
Mitigation: Review heartbeat behavior, timeouts, and routing rules before enabling automation in a shared workspace. <br>
Risk: Bulk cleanup, dead-letter, or queue maintenance commands can remove operational history or important failure state. <br>
Mitigation: Preview or export queue and dead-letter state before running cleanup, drain, archive, or clear commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with bash, YAML, TypeScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes task schema, CLI workflows, heartbeat integration, routing strategies, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
