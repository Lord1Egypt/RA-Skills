## Description:

Executes background tasks safely by dropping privileges and enforcing timeouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horn111](https://clawhub.ai/user/horn111)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to run agent-triggered background commands with timeout handling, privilege dropping, and structured execution logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports privilege, timeout, logging, and release-verification weaknesses that reduce confidence in the skill's safety claims.

Mitigation: Review before installation, avoid privileged or multi-user environments, and require fixes for supplementary groups, process-group termination, secure logging, and version-matched signed manifests before production use.

Risk: The skill writes command previews to a /tmp log, which may expose sensitive command output or provide weak audit storage.

Mitigation: Avoid running secret-bearing commands and route logs to controlled storage with appropriate permissions before production deployment.

Risk: The command wrapper is not a complete sandbox.

Mitigation: Use it only as a constrained command runner and pair it with external isolation, command allowlists, and human review for high-impact tasks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/horn111/skills/safe-cron-runner)
- [ISNAD Manifest](isnad_manifest.json)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code examples and JSON execution results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured task status, duration, stdout preview, stderr preview, and log entries.]

## Skill Version(s):

1.0.2 (source: frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
