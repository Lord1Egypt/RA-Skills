## Description: <br>
Configure, deploy, and troubleshoot web servers, application servers, and containerized services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to configure web servers, reverse proxies, process managers, TLS certificates, Docker Compose services, and common self-hosted application patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server administration commands and configuration examples can affect live services if copied without review. <br>
Mitigation: Review every command before running it on a production host and adapt examples to the target environment. <br>
Risk: Example credentials and environment values can expose secrets if reused directly. <br>
Mitigation: Replace example passwords and protect secrets with an ignored .env file, Docker secrets, or a secret manager. <br>
Risk: The Traefik example includes an insecure dashboard/API flag that is unsuitable for production as written. <br>
Mitigation: Remove or secure the insecure dashboard/API flag before deploying Traefik publicly. <br>
Risk: Persistent services and Docker volume deletion can cause data loss or prolonged service changes. <br>
Mitigation: Confirm persistence, backups, and the impact of destructive Docker commands before deleting volumes or changing long-running services. <br>


## Reference(s): <br>
- [Server Configuration Examples](configs.md) <br>
- [Docker and Docker Compose Patterns](docker.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
