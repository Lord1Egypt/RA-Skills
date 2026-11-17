## Description:

Setup completo de VPS Ubuntu/Debian para produção com Docker Swarm, Traefik v3 (SSL/HTTPS automático), Portainer CE e rede overlay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[impa365](https://clawhub.ai/user/impa365)

### License/Terms of Use:


## Use Case:

Developers and system administrators use this skill to set up an Ubuntu or Debian VPS with Docker Swarm, Traefik HTTPS routing, Portainer CE, PostgreSQL, Redis, and Evolution API deployment steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs broad privileged server changes that can alter a VPS, Docker daemon, networking, and service exposure.

Mitigation: Review every command before execution and use only on a dedicated VPS that can be rebuilt.

Risk: The setup uses insecure bootstrap and dependency practices, including curl-piped installation and unpinned container images.

Mitigation: Use verified package-repository installation and pin container images by version or digest before running.

Risk: TLS validation is bypassed in several Portainer API commands and Portainer agent configuration.

Mitigation: Remove curl -k and --tlsskipverify usage and ensure services use valid certificates.

Risk: Tokens, passwords, and API keys may be printed or embedded in generated files and logs.

Mitigation: Use Docker secrets or another secret manager, avoid printing credentials, and rotate any exposed credentials.

Risk: Administrative services may be reachable from untrusted networks after deployment.

Mitigation: Restrict Portainer and other administrative endpoints to trusted administrative networks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/impa365/skills/setuporion-byimpa)
- [Docker install bootstrap](https://get.docker.com)
- [Facebook Graph API](https://graph.facebook.com)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment-variable driven setup commands and verification steps for a privileged VPS deployment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
