## Description: <br>
WSL2 Local AI guides Windows developers through running local LLM workflows in WSL2 with NVIDIA GPU passthrough, Ollama, CUDA, Docker, and Ollama Herd routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up a Windows and WSL2 local AI development stack, route requests through Ollama Herd, and connect tools such as VS Code, Python, curl, and Docker to local model endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup includes commands that execute downloaded installer code, install packages, and run local background services. <br>
Mitigation: Review the remote Ollama installer and the ollama-herd package source before running commands, and only run the services needed for the local development environment. <br>
Risk: The workflow can create local state under ~/.fleet-manager and optionally add persistent shell settings to ~/.bashrc. <br>
Mitigation: Review persistence commands before applying them, track local configuration changes, and avoid deleting or modifying ~/.fleet-manager outside the documented workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/wsl2-local-ai) <br>
- [Ollama Herd repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown with PowerShell, bash, Python, JSON, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target Windows with WSL2 and assume user-controlled model downloads, deletions, and service startup.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
