## Description:

Manage a shared Redis Docker container for local dev environments, including container lifecycle, key inspection, and selective data flush.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pereirajair](https://clawhub.ai/user/pereirajair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to start, stop, inspect, and clean a local Redis service shared by Docker-based development environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default Redis password is known and the container joins a shared Docker network.

Mitigation: Set a strong REDIS_PASSWORD before starting Redis and limit which containers can join the shared Docker network.

Risk: Flush commands can permanently delete Redis data.

Mitigation: Treat flush and flush-db as destructive operations and rely on their confirmation prompts only after checking the target database or environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pereirajair/skills/redis-manager)
- [Publisher profile](https://clawhub.ai/user/pereirajair)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes Docker is available on Linux or macOS and that the shared Docker network exists before Redis starts.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.1.0 and _meta.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
