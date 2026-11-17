## Description:

Deploy self-hosted applications to any VPS with Docker Compose, including app-specific configurations, Nginx reverse proxy setup, SSL via Certbot, backups, resource limits, and health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llcsamih](https://clawhub.ai/user/llcsamih)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and generate VPS deployment steps for common self-hosted applications using Docker Compose, reverse proxying, TLS, backups, and health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for privileged VPS access and may lead users to run administrative deployment commands.

Mitigation: Use a temporary least-privileged deployment account, avoid sharing SSH passwords or private keys in chat, and review every command before execution.

Risk: Some generated deployment patterns may expose sensitive services or host control surfaces, including Docker socket mounts and administrative interfaces.

Mitigation: Remove unnecessary Docker socket mounts, bind admin interfaces to localhost or a VPN, and expose only reviewed services through the reverse proxy.

Risk: Unpinned images, remote installers, unchecked user-provided values, and cron jobs can create supply-chain or persistence risk.

Mitigation: Pin container images and installers, validate domain, application, and path values, and explicitly approve any scheduled backup or maintenance cron job.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/llcsamih/skills/self-host-deployer)
- [Supabase Self-Hosting API Keys Documentation](https://supabase.com/docs/guides/self-hosting#api-keys)
- [Supabase Docker Repository](https://github.com/supabase/supabase)
- [Immich Docker Compose Release Asset](https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml)
- [Immich Example Environment Release Asset](https://github.com/immich-app/immich/releases/latest/download/example.env)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with YAML, environment variable, Nginx, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates deployment-oriented instructions and configuration snippets for the selected self-hosted application.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
