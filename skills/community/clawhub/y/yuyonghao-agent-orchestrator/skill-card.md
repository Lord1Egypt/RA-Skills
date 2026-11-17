## Description:

Agent Orchestrator provides a JavaScript in-memory orchestration library for agent lifecycle management, task scheduling, resource tracking, health checks, service discovery, and cluster coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill as a JavaScript library sample for coordinating registered agents, routing tasks by capability, and monitoring basic health and resource status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resource-limit behavior may not provide production-grade isolation for multi-tenant workloads.

Mitigation: Treat CPU, memory, and concurrency controls as advisory until scheduler and resource-manager enforcement is hardened and independently tested.

Risk: Documentation is Chinese-only, which may increase integration or operations mistakes for teams that cannot review it directly.

Mitigation: Require a fluent reviewer or approved translation before deploying or modifying the package in a production workflow.

Risk: The package is best treated as a prototype or library sample despite production-oriented feature claims.

Mitigation: Use it behind additional runtime safeguards and validate health checks, recovery behavior, and task cancellation under representative load before commercial deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-agent-orchestrator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
