## Description:

Redis 缓存和数据结构管理技能。通过自然语言操作 Redis，支持 String、Hash、List、Set、ZSet、Stream 等数据结构操作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanlee-gemini](https://clawhub.ai/user/ryanlee-gemini)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and backend engineers use this skill to draft Redis commands and configuration guidance for caching, object storage, queues, leaderboards, distributed locks, streams, and performance analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Redis commands can change or delete production data, especially configuration, Lua EVAL, reset, and range-delete operations.

Mitigation: Confirm the target host, database, backup posture, and command impact before running generated commands.

Risk: Installation guidance includes privileged or environment-changing commands such as sudo, brew, and pip installs.

Mitigation: Review setup commands before execution and run them only in an environment the user administers.

Risk: Redis deployments may expose sensitive data or administrative access if authentication, network isolation, or permissions are misconfigured.

Mitigation: Use Redis authentication, network isolation, least-privilege deployment patterns, and encryption for sensitive data where appropriate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ryanlee-gemini/skills/redis-skill)
- [Redis Documentation](https://redis.io/docs/)
- [Redis Commands](https://redis.io/commands/)
- [Redis Latency Documentation](https://redis.io/topics/latency)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Redis CLI commands, Python redis client snippets, and operational guidance that should be reviewed before execution against live databases.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
