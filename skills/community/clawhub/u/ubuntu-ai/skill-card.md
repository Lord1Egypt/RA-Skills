## Description: <br>
Ubuntu AI helps agents guide users through building a local AI platform on Ubuntu or Debian for LLM inference, image generation, embeddings, and heterogeneous CPU, NVIDIA CUDA, AMD ROCm, x86, and ARM deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up and operate a local Ubuntu or Debian AI service with Ollama Herd, including package installation, systemd services, GPU checks, firewall configuration, monitoring endpoints, and OpenAI-compatible usage examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup can open port 11435 and expose a local AI service beyond the host if network access is broadened. <br>
Mitigation: Keep the service bound to localhost by default; if remote access is required, restrict source IPs and add authentication, TLS, or a hardened reverse proxy. <br>
Risk: The quick start installs upstream software and Python packages that may change outside the skill release. <br>
Mitigation: Review the Ollama installer and the ollama-herd package before running installation commands, and pin or audit versions where operational controls require it. <br>
Risk: The systemd and firewall examples make persistent privileged changes to the machine. <br>
Mitigation: Review each privileged command before execution, document the service and firewall changes, and plan rollback steps before enabling them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/ubuntu-ai) <br>
- [Ollama Herd project](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash, Python, service-unit, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include privileged Linux setup steps, persistent service configuration, local HTTP endpoints, and package installation commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
