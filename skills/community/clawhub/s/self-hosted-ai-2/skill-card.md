## Description: <br>
Self Hosted Ai helps users deploy, operate, and troubleshoot self-hosted AI tools such as Ollama, N8N, Open WebUI, Docker, nginx, and HTTPS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nima54851](https://clawhub.ai/user/nima54851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill for deployment and operations guidance when setting up local or self-hosted AI services on servers they control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested deployment commands may download install scripts, change service configuration, or affect running server workloads. <br>
Mitigation: Review commands and downloaded scripts before execution, and test changes in a controlled environment before applying them to production systems. <br>
Risk: Binding services such as Ollama or N8N to 0.0.0.0 can expose them beyond the local host if network controls are not configured. <br>
Mitigation: Expose services only when remote access is intentional, and protect them with firewall rules, TLS, strong credentials, and a reverse proxy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nima54851/skills/self-hosted-ai-2) <br>
- [Server-resolved GitHub source](https://github.com/nima54851/agent-studio/tree/main/skills/self-hosted-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, Docker Compose, and nginx configuration code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance output should be reviewed and adapted before commands are run on live servers.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
