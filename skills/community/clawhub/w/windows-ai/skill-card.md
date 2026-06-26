## Description: <br>
Windows AI helps agents guide local AI setup on Windows PCs for LLM inference, image generation, embeddings, and OpenAI-compatible access through an Ollama Herd endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Windows users use this skill to configure and operate a local Windows AI cluster for private LLM, image generation, and embedding workloads. It provides setup commands, OpenAI-compatible examples, hardware guidance, and integration notes for tools such as Cursor, LangChain, CrewAI, and Open WebUI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides users to expose a local AI router on port 11435 for LAN access, and the security evidence warns that this may expose an unauthenticated AI service. <br>
Mitigation: Avoid opening the firewall for local-only use; if LAN access is needed, restrict port 11435 to trusted private devices and confirm authentication or allowlist support before sending sensitive prompts. <br>
Risk: The skill depends on the ollama-herd package source and local cluster behavior. <br>
Mitigation: Install only when the package source is trusted, and review commands before running them on Windows hosts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/windows-ai) <br>
- [Ollama Herd Repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Ollama Herd Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [Ollama Herd API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with PowerShell, Python, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets Windows systems; requires curl or wget and can optionally use python3, pip, and nvidia-smi.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
