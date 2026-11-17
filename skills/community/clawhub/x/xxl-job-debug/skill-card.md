## Description:

Use when triggering or debugging XXL-JOB tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrd77](https://clawhub.ai/user/jrd77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to manage and debug XXL-JOB scheduler tasks, including resolving executors, triggering jobs, inspecting logs, and handling local IntelliJ/JVM debug flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents through kill, delete, start, stop, update, or production trigger operations that may affect running XXL-JOB workloads.

Mitigation: Require the agent to show the exact jobId, appName, executor, and expected impact, then obtain explicit confirmation before performing these operations.

Risk: XXL-JOB access tokens could be exposed while resolving scheduler or executor connections.

Mitigation: Use least-privileged tokens and never print the full token in outputs or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jrd77/skills/xxl-job-debug)

## Skill Output:

**Output Type(s):** [guidance, API calls, shell commands, configuration]

**Output Format:** [Markdown with inline HTTP, JSON, YAML, properties, Java, and text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operation-focused responses with resolved job, executor, handler, log, status, result, and evidence fields when applicable.]

## Skill Version(s):

4.0.0 (source: server evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
