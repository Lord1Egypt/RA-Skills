## Description:

Queue async tasks for your agent with retry logic, priority levels, dependency chains, concurrency, per-task timeouts, event hooks, cancel/clear, and run metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to organize asynchronous work into ordered or concurrent queues with priorities, retries, dependencies, timeouts, cancellation, and run metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tasks can run without a timeout by default, which may leave an agent waiting on long-running or stalled work.

Mitigation: Configure finite global or per-task timeouts for queues that call external systems or untrusted handlers.

Risk: Automatic retries can repeat actions that publish, delete, charge, or otherwise mutate external systems.

Mitigation: Keep retry counts low and only enable retries for idempotent tasks or handlers with explicit duplicate-protection.

Risk: Untrusted task definitions can create unsafe dependency structures or unexpected execution behavior.

Mitigation: Validate task IDs, dependency chains, priorities, retry counts, and timeouts before enqueueing externally supplied tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/task-queue-sr)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [code, configuration, guidance]

**Output Format:** [JavaScript module with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces in-memory queue execution results, task statuses, retry counts, logs, metrics, and event notifications.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
