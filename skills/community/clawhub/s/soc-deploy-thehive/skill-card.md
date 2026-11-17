## Description:

Deploys TheHive 5 and Cortex 3 on a Docker-ready Linux host and guides account setup, API key generation, CSRF-aware Cortex setup, and TheHive-Cortex integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Security engineers, SOC operators, and infrastructure developers use this skill to deploy a TheHive and Cortex incident response stack on an SSH-accessible Linux host with Docker. It is intended for setup automation and integration guidance, not VM provisioning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployment uses insecure defaults and can expose high-value administrator credentials and service endpoints.

Mitigation: Review and harden the deployment before installation, use a strong explicit password, run setup only on an isolated or firewalled host, and bind services to localhost during bootstrap when possible.

Risk: Generated credentials and API keys are written to plaintext output and a credentials file.

Mitigation: Protect or remove the credentials file, avoid logging setup output, and rotate generated keys after setup.

Risk: Shell and JSON interpolation can be unsafe if untrusted input is accepted for passwords, organization names, or secrets.

Mitigation: Fix unsafe interpolation before accepting untrusted input and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/solomonneas/skills/soc-deploy-thehive)
- [API Reference: TheHive + Cortex](references/api-reference.md)
- [Docker Compose configuration](references/docker-compose.yml)
- [Gotchas: TheHive + Cortex Deployment](references/gotchas.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deployment URLs, administrator credentials, API keys, MCP connection environment variables, and file paths for saved credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
