## Description: <br>
Windows Ollama helps agents guide Windows users through running Ollama with fleet routing, load balancing, health monitoring, and dashboard access across multiple Windows PCs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Windows AI users use this skill to set up Ollama Herd, route Ollama inference across multiple Windows machines, monitor fleet health, and configure local model-serving behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup exposes an Ollama router on TCP port 11435, which could be reachable by untrusted systems if firewall scope is too broad. <br>
Mitigation: Run the router only on trusted Windows machines and restrict port 11435 to private networks or specific trusted source IPs. <br>
Risk: The workflow installs and runs the third-party ollama-herd package. <br>
Mitigation: Verify the package and project before installation, then review commands before execution. <br>
Risk: Persistent Ollama environment settings and firewall rules can outlive the intended test or deployment window. <br>
Mitigation: Remove the firewall rule and persistent Ollama environment settings when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/windows-ollama) <br>
- [Ollama download](https://ollama.ai) <br>
- [Ollama Herd agent setup guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [Ollama Herd API reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with PowerShell, Python, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets Windows systems and local network Ollama endpoints; no API key requirement is declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
