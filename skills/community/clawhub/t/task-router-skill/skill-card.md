## Description:

Distributed task queue and agent coordinator for OpenClaw multi-agent systems that routes tasks by capability, tracks lifecycle state, coordinates async handoffs, rebalances workloads, and manages dead letters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[capt-marbles](https://clawhub.ai/user/capt-marbles)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to coordinate OpenClaw multi-agent work through capability-based task routing, lifecycle tracking, retries, dead-letter review, and asynchronous handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The task router persists queue, agent registry, completion, failure, and log state under the OpenClaw task-router directory.

Mitigation: Enable the router only in workspaces where persistent task state is expected, and review stored queue data and logs before sharing or archiving the workspace.

Risk: Automatic routing, heartbeat, cron, cancel, clear, cleanup, and dead-letter commands can reassign, retry, archive, or remove queued work.

Mitigation: Review heartbeat or cron configuration before enabling automation, keep registered agent capabilities narrow, and inspect queued work before running maintenance commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, YAML, and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes CLI examples, configuration schemas, task lifecycle guidance, and TypeScript API examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
