## Description: <br>
Setup completo de VPS Ubuntu/Debian para producao com Docker Swarm, Traefik v3, SSL/HTTPS automatico, Portainer CE e rede overlay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[impa365](https://clawhub.ai/user/impa365) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to prepare an Ubuntu or Debian VPS for production-style Docker Swarm hosting with Traefik, Portainer, PostgreSQL, Redis, and Evolution API services. It provides ordered setup, deployment, verification, maintenance, and troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup performs broad privileged server changes and deploys persistent administrative services. <br>
Mitigation: Install only on a fresh VPS you control, review each command before execution, prefer snapshots or backups before starting, and treat Portainer API examples as full administrative access. <br>
Risk: The workflow handles admin credentials and tokens in command output, YAML files, and credential-bearing curl calls. <br>
Mitigation: Use strong generated secrets, avoid printing tokens or passwords, remove insecure TLS bypass flags from credential-bearing curl commands, restrict access to generated files, and rotate credentials after setup. <br>
Risk: The Docker installation path can execute remote shell content during setup. <br>
Mitigation: Prefer the signed Docker repository installation path when possible and review downloaded installation commands before running them with elevated privileges. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/impa365/setuporion-byimpa) <br>
- [Docker installation script](https://get.docker.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces ordered VPS setup and verification steps using user-provided hostname, domain, email, network, and credential environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
