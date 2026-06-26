## Description: <br>
Deploy production-ready self-hosted applications to any VPS with Docker Compose, Nginx, SSL, backups, and health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[llcsamih](https://clawhub.ai/user/llcsamih) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to select and deploy self-hosted open-source applications on VPS infrastructure using Docker Compose, Nginx, SSL certificates, backups, resource limits, and health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for VPS access details and can guide changes with broad control over a server. <br>
Mitigation: Use key-based SSH with a dedicated sudo-capable account, avoid pasting private keys or long-lived passwords into chat, and inspect generated commands before running them. <br>
Risk: Some deployment options expose high-trust Docker host controls, including Portainer, Dockge, and Docker socket mounts. <br>
Mitigation: Treat Docker host access as privileged, enable these options only when needed, restrict network exposure, and review each socket mount or management UI before deployment. <br>
Risk: Installer and setup commands, including curl-pipe-bash patterns, can make significant host changes. <br>
Mitigation: Review installer contents and generated shell commands first, run them manually on infrastructure you own, and keep backups or rollback steps available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/llcsamih/self-host-deployer) <br>
- [Supabase self-hosting API keys](https://supabase.com/docs/guides/self-hosting#api-keys) <br>
- [Supabase Docker repository](https://github.com/supabase/supabase) <br>
- [Immich Docker Compose release file](https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Docker Compose YAML, shell commands, Nginx and Certbot configuration, backup scripts, and deployment checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include app-specific deployment plans, generated secrets placeholders, health checks, and post-deploy verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
