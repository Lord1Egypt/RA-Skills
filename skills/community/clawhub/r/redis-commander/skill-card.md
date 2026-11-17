## Description:

Manage the Redis Commander Docker container for local development environments, providing a local web UI for Redis key inspection and management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pereirajair](https://clawhub.ai/user/pereirajair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to start, stop, inspect, and access a local Redis Commander container while working with Redis-backed development environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default Redis Commander and Redis credentials are weak for shared machines.

Mitigation: Set unique COMMANDER_USER, COMMANDER_PASSWORD, and REDIS_PASSWORD values before starting the container.

Risk: The Redis Commander container image is referenced with the latest tag.

Mitigation: Prefer a pinned Redis Commander image version or digest before routine use.

Risk: The tool can inspect and modify Redis data.

Mitigation: Run it only on trusted local development machines, keep the port bound to localhost, and stop the container when finished.

## Reference(s):

- [Redis Commander ClawHub Skill Page](https://clawhub.ai/pereirajair/skills/redis-commander)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker on Linux or macOS and existing proxy-manager and redis-manager services.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
