## Description:

Install, configure, start, stop, and verify local or remote development infrastructure across Windows, Linux, and macOS by executing commands through a unified workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, execute, verify, and persist state for local or remote setup of common development infrastructure such as Redis, PostgreSQL, MySQL, MinIO, ZLMediaKit, Docker, Nginx, Node.js, Python, and Java.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MinIO recipe includes predictable root credentials that could expose a deployed storage service.

Mitigation: Replace the default MinIO credentials with unique generated secrets or a secret manager value before deployment, and bind MinIO only to trusted networks.

Risk: The skill can execute local or remote shell commands and may use elevated privileges for infrastructure changes.

Mitigation: Confirm the target host, transport, privilege level, and exact commands before execution, especially for remote nodes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hgvgfgvh/skills/universal-shell-deployer)
- [Publisher profile](https://clawhub.ai/user/hgvgfgvh)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with command plans, shell commands, verification results, and configuration state summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update the skill's config.json state after meaningful progress.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
