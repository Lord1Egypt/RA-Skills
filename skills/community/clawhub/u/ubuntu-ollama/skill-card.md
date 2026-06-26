## Description: <br>
Ubuntu Ollama helps agents set up and operate Ollama fleet routing on Ubuntu with apt, systemd, CUDA-aware checks, health monitoring, and API examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and system administrators use this skill to configure an Ubuntu-based Ollama router, register additional Ubuntu nodes, run services with systemd, and test local inference endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to install remote software and packages on Ubuntu hosts. <br>
Mitigation: Review the Ollama installer and ollama-herd package before use, pin versions where possible, and run services under a dedicated low-privilege user. <br>
Risk: The skill configures persistent services and exposes an inference router, dashboard, and health endpoints on port 11435. <br>
Mitigation: Restrict port 11435 to trusted hosts or a VPN, and do not expose the dashboard or inference API broadly without authentication and TLS. <br>
Risk: The security review notes limited safety guidance for a networked Ollama fleet setup. <br>
Mitigation: Review the commands before execution, apply local security controls, and confirm model downloads or deletions explicitly. <br>


## Reference(s): <br>
- [Ubuntu Ollama on ClawHub](https://clawhub.ai/twinsgeeks/ubuntu-ollama) <br>
- [Ollama Herd repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, Python, JSON, and systemd configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Ubuntu package, pip, systemd, firewall, monitoring, and API usage guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
