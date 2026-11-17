## Description:

Self Hosted Ai helps developers and operators deploy and troubleshoot self-hosted AI tools including Ollama, N8N, Open WebUI, Docker Compose, nginx reverse proxying, and HTTPS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nima54851](https://clawhub.ai/user/nima54851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate deployment commands, configuration guidance, and troubleshooting steps for self-hosted AI services on servers. It is intended for operating local model runtimes, workflow automation, web UI access, reverse proxies, and HTTPS setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes commands that may execute mutable remote installer code.

Mitigation: Review installer commands before use and prefer verified package or release installation for Ollama where available.

Risk: The skill shows service bindings and port mappings that can expose Ollama, N8N, or web interfaces beyond localhost.

Mitigation: Bind services to localhost by default and expose remote access only through authenticated TLS, a VPN, or a restricted reverse proxy.

Risk: Container images and service credentials may be unsafe if left at mutable defaults.

Mitigation: Pin container image versions and set strong N8N credentials before exposing any service.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/nima54851/agent-studio/tree/main/skills/self-hosted-ai)
- [ClawHub skill page](https://clawhub.ai/nima54851/skills/self-hosted-ai-2)
- [Ollama installer referenced by the skill](https://ollama.com/install.sh)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash, YAML, and nginx configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deployment steps, environment variables, container configuration, reverse proxy snippets, and troubleshooting commands.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
