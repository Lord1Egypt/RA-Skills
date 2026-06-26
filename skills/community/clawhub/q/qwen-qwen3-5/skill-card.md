## Description: <br>
Guides agents through running Qwen-family models across a local Ollama Herd device fleet, including setup commands, API examples, monitoring, hardware guidance, and guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up and operate a local Ollama Herd fleet for Qwen-family inference, coding, and speech-to-text workflows. It provides shell commands, Python and API request examples, monitoring endpoints, and safety guardrails for local model serving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the referenced Ollama Herd package executes third-party PyPI code. <br>
Mitigation: Review the PyPI package and repository before installation, and install only in environments where the package and dependencies are trusted. <br>
Risk: The router, dashboard, status endpoints, and local logs may expose operational usage details. <br>
Mitigation: Run the service only on trusted networks and treat dashboard responses and ~/.fleet-manager logs as local operational data. <br>
Risk: Qwen model downloads can be large and may affect disk, memory, or bandwidth budgets. <br>
Mitigation: Keep model pulls user-confirmed and choose model sizes that match the available device RAM and storage. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/twinsgeeks/qwen-qwen3-5) <br>
- [Ollama Herd repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Ollama Herd PyPI package](https://pypi.org/project/ollama-herd/) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, Python, and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local endpoint examples, hardware recommendations, and operational guardrails.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
