## Description: <br>
Deploy a full-stack app to a VPS by guiding server setup, Docker deployment, Nginx reverse proxy, SSL certificates, and post-deploy health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[llcsamih](https://clawhub.ai/user/llcsamih) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to take a local full-stack app to a bare Ubuntu/Debian VPS by configuring SSH, firewall, Docker Compose, Nginx, SSL, and verification checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change SSH and firewall settings on a VPS, which could lock out administrators or disrupt access. <br>
Mitigation: Use a fresh or backed-up server, keep an existing SSH session open, and verify deploy-user SSH access before disabling root login. <br>
Risk: The skill can modify Nginx and deployment configuration on a live server. <br>
Mitigation: Back up existing Nginx configs first, run configuration tests before reloads, and review generated deployment files before applying them. <br>
Risk: The skill installs Docker from an external script and creates a deploy user with passwordless sudo. <br>
Mitigation: Review the Docker install command before execution and remove or restrict passwordless sudo when deployment is complete. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/llcsamih/vps-deploy) <br>
- [Docker installation script endpoint](https://get.docker.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, Dockerfile, YAML, and Nginx configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce server administration commands, deployment files, and verification checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
