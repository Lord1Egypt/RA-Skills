## Description: <br>
Queue async tasks for your agent with retry logic, priority levels, dependency chains, concurrency, per-task timeouts, event hooks, cancel/clear, and run metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use TaskQueue to orchestrate asynchronous agent workflows with priorities, retries, dependency chains, concurrency controls, timeouts, cancellation, logs, and run metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queued handlers can perform costly, destructive, public, or account-changing actions, and the queue will execute and retry whatever functions are provided. <br>
Mitigation: Use explicit timeouts, conservative retry counts, low concurrency, and review queued handlers before running them. <br>
Risk: Long-running or stuck task handlers can delay the queue when no timeout is configured. <br>
Mitigation: Set default or per-task timeouts for workflows that call external services or perform slow operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TheShadowRose/task-queue-sr) <br>
- [README.md](artifact/README.md) <br>
- [TaskQueue source](artifact/src/task-queue.js) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [JavaScript module API returning JSON-like task summaries, logs, results, and metrics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [In-memory queue execution with configurable retries, retry delay, concurrency, task dependencies, per-task timeouts, cancellation, clearing, pause/resume, event hooks, and metrics.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
