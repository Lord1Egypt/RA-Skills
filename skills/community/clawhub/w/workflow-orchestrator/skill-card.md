## Description:

Workflow Orchestrator helps agents build and run DAG-based multi-agent workflows with branching, parallel execution, retry logic, fallback handling, and live monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to define and run multi-agent workflows where steps can execute in dependency order, fan out in parallel, retry on failure, use fallbacks, and expose workflow status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented condition controls may fail open and allow consequential workflow steps to run when conditions are malformed or unsupported.

Mitigation: Review and test conditions with trusted workflow definitions before using them for consequential actions; harden condition evaluation before relying on it as a safety boundary.

Risk: Documented timeout controls may not stop long-running registered executors, which can hang workflows or leave consequential steps running.

Mitigation: Use trusted executors with external timeout or cancellation controls, and validate timeout handling before connecting workflows to agents that publish, deploy, or modify data.

Risk: Workflow definitions and registered executors can direct agents to send messages, publish content, deploy, or modify data.

Mitigation: Treat workflow definitions and executor registrations as trusted code, and review them before running with real agents or sensitive data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/evezart/skills/workflow-orchestrator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workflow definitions, runner usage patterns, and operational guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
