## Description: <br>
Self Evolve helps an agent run measured self-improvement cycles by identifying bottlenecks, comparing candidate solutions, recording observations, and solidifying successful workflow or tool changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikonos](https://clawhub.ai/user/mikonos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill when they want an AI agent to run disciplined, measurable experiments for improving its own tools, workflows, schedules, or meta-capabilities. It is suited to environments where self-modification is intentional and governed by review, rollback, and command approval controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to experiment on and permanently change its own behavior, tools, workflows, or configuration. <br>
Mitigation: Run it in a sandboxed environment, keep backups for rollback, and require review before solidifying any code, configuration, cron, heartbeat, or behavior change. <br>
Risk: The skill can direct shell commands, external searches, installs, or deployments as part of experiments. <br>
Mitigation: Require explicit approval for shell commands, external installs, and code or configuration diffs; disable cron or heartbeat automation by default. <br>
Risk: Writable memory and evolution state files can steer future self-modification if untrusted content is introduced. <br>
Mitigation: Protect memory/evolve files from untrusted writes and review candidate queues, reports, and telemetry before the agent acts on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikonos/self-evolve-agent) <br>
- [Execution protocol and state machine](references/execution-protocol.md) <br>
- [Constraints and autonomy rules](references/constraints-and-rules.md) <br>
- [Quality checklist](references/quality-checklist.md) <br>
- [Evolution report template](assets/evolution-report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports and plans with YAML frontmatter, JSONL observations, state updates, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update memory/evolve reports, state.json, JSONL logs, and agent configuration or workflow files when the host agent is allowed to make those changes.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
