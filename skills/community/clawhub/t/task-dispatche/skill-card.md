## Description:

Dispatches scheduled workload tasks to worker nodes for execution and records dispatch logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink5725](https://clawhub.ai/user/ink5725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to convert scheduled workload reports into dispatch records for task execution tracking, audit review, and recovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may report tasks as dispatched without actually delivering work to worker nodes.

Mitigation: Treat it as a local dispatch-log writer until real worker delivery and delivery verification are added.

Risk: The skill writes dispatch records to a system log path.

Mitigation: Run it under a least-privileged account with a tightly owned log directory or a safer application-owned path.

## Reference(s):


## Skill Output:

**Output Type(s):** [JSON, Files]

**Output Format:** [JSON dispatch summary and per-task JSON dispatch log records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes dispatch records under /var/log/compute/dispatched when executed with sufficient permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
