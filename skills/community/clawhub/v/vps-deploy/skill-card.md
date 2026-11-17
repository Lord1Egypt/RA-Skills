## Description:

Deploy a full-stack app to any VPS from zero to production in one command, including SSH hardening, firewall setup, Docker, Nginx reverse proxy, SSL certificates, and health verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llcsamih](https://clawhub.ai/user/llcsamih)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy an application from a local project to a fresh Ubuntu or Debian VPS with Docker, Nginx, optional TLS, and post-deployment checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad, permanent root-level VPS changes that may expose or break a server if followed without review.

Mitigation: Use it only on a fresh or dedicated VPS, review commands before execution, and require explicit confirmation before SSH, firewall, Nginx, or destructive changes.

Risk: The Docker installation flow uses curl-to-shell, and the deployment flow may create unrestricted passwordless sudo or reuse root SSH keys.

Mitigation: Prefer a verified package workflow for Docker, use a dedicated deploy public key, avoid unrestricted passwordless sudo, and back up Nginx configs before changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/llcsamih/skills/vps-deploy)
- [Publisher Profile](https://clawhub.ai/user/llcsamih)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, Dockerfile, YAML, and Nginx configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated Dockerfile and docker-compose.yml content, remote SSH commands, Nginx site configuration, certificate setup commands, and verification checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
