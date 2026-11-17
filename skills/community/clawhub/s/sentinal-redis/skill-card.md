## Description:

Monitor Redis server health, memory, performance, and BullMQ queues. Check queue depths, inspect failed jobs, analyze slow queries, and diagnose issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[musaraf-m](https://clawhub.ai/user/musaraf-m)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run read-only diagnostics for Redis health, memory, latency, slow queries, client state, and BullMQ queue status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Redis credentials and diagnostic output may contain sensitive connection details, application data, job payloads, or secrets.

Mitigation: Use the skill only where read-only Redis diagnostics are authorized, prefer a least-privilege Redis user, mask REDIS_URL credentials, and review slow-log or BullMQ job output before sharing reports.

Risk: Diagnostics run against the wrong Redis instance can inspect unintended data.

Mitigation: Confirm the target REDIS_URL or localhost default before running commands, and ask for confirmation when scope is unclear.

## Reference(s):

- [Sentinal Redis ClawHub Skill Page](https://clawhub.ai/musaraf-m/skills/sentinal-redis)
- [musaraf-m Publisher Profile](https://clawhub.ai/user/musaraf-m)
- [Redis Commands Quick Reference](references/redis-commands.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and diagnostic summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires redis-cli and optionally REDIS_URL; diagnostic output may include sensitive Redis metadata or job data.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
