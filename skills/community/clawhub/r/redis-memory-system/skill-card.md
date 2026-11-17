## Description:

Fully automatic cross-session short-term memory system with a single script, configuration-driven operation, and a semantic tag index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hualang-c](https://clawhub.ai/user/hualang-c)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install and operate a Redis-backed memory helper that syncs recent session dialogue summaries, retrieves recent memory, searches semantic tags, and checks memory-system status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill ingests cross-session transcript content into Redis, which can include sensitive user or session information.

Mitigation: Use an opt-in installation path, treat stored summaries and transcript excerpts as sensitive data, and avoid shared Redis databases.

Risk: The setup script registers persistent cron-based background execution.

Mitigation: Manually review or remove cron registration before deployment, and approve scheduled execution only for intended users and environments.

Risk: Redis-backed memory can be exposed if Redis access is broad or unauthenticated.

Mitigation: Restrict Redis access, validate configured usernames, and isolate memory data per user or deployment.

## Reference(s):

- [Redis Memory System README](artifact/README.md)
- [ClawHub Skill Page](https://clawhub.ai/hualang-c/skills/redis-memory-system)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Redis memory operations for sync, get, set, tag search, heartbeat, ping, and stats workflows.]

## Skill Version(s):

3.3.0 (source: server release evidence, artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
