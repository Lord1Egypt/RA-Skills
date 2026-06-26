## Description: <br>
Deploy TheHive 5 + Cortex 3 incident response platform on any Docker-ready Linux host. Automates account creation, API key generation, Cortex CSRF handling, and TheHive-Cortex integration wiring. Platform-agnostic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security operations engineers and developers use this skill to deploy a TheHive and Cortex incident response stack on an existing SSH-accessible Linux host with Docker. It helps automate service startup, administrator setup, API key creation, and TheHive-Cortex integration wiring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles powerful TheHive and Cortex administrator credentials and API keys during deployment. <br>
Mitigation: Use a strong unique password, store generated keys securely, delete or lock down ~/thehive-cortex/api-keys.txt, and rotate keys if they appear in logs or transcripts. <br>
Risk: The deployed TheHive and Cortex services expose ports 9000 and 9001 on the target host. <br>
Mitigation: Install only on a trusted lab or tightly controlled host and restrict access with firewall rules, VPN, or TLS. <br>
Risk: Routine automation with a Cortex superadmin key can grant broader access than needed. <br>
Mitigation: Prefer the Cortex org-admin key instead of the superadmin key for routine MCP or integration use. <br>


## Reference(s): <br>
- [API Reference: TheHive + Cortex](references/api-reference.md) <br>
- [Docker Compose Stack](references/docker-compose.yml) <br>
- [Gotchas: TheHive + Cortex Deployment](references/gotchas.md) <br>
- [ClawHub skill page](https://clawhub.ai/solomonneas/soc-deploy-thehive) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and deployment configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment steps, service URLs, credentials handling guidance, and MCP connection environment values.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
