## Description: <br>
Rtx Local Ai helps developers and AI builders turn Windows or Linux NVIDIA RTX gaming PCs into local Ollama Herd AI servers for model inference, code generation, image generation, embeddings, monitoring, and fleet routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and AI builders use this skill to configure RTX-equipped PCs as local AI servers and route requests across one or more machines. It supports local workflows for chat completions, code generation, image generation, embeddings, fleet monitoring, and Ollama configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing and running Ollama Herd from an untrusted package source could introduce unwanted software or configuration changes. <br>
Mitigation: Install only after trusting the Ollama Herd project and package source, and prefer a virtual environment or container. <br>
Risk: Fleet mode can expose local AI services on a LAN if networking is not reviewed. <br>
Mitigation: Review LAN exposure, host binding, and firewall settings before enabling fleet mode. <br>
Risk: System service edits and sudo commands can affect host configuration. <br>
Mitigation: Review systemd or environment changes before applying them and limit changes to the documented Ollama settings. <br>
Risk: Large model downloads can consume significant storage and bandwidth. <br>
Mitigation: Require explicit user confirmation before model downloads or deletions. <br>


## Reference(s): <br>
- [Ollama Herd GitHub Repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Ollama Herd PyPI Package](https://pypi.org/project/ollama-herd/) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell, Python, PowerShell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local endpoint examples and RTX/Ollama configuration guidance; model downloads and deletions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
