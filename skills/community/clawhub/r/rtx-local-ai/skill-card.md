## Description:

RTX Local AI helps developers and AI builders set up an NVIDIA RTX Windows or Linux PC, or a small RTX fleet, as a local Ollama Herd server for LLM inference, image generation, embeddings, monitoring, and OpenAI-compatible API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI builders, and technical users use this skill to configure local RTX hardware for Ollama Herd routing, OpenAI-compatible requests, fleet monitoring, and model-serving workflows without relying on cloud inference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing `ollama-herd` directly from PyPI can introduce ordinary dependency and supply-chain risk.

Mitigation: Review the PyPI/GitHub project before installation and use a virtual environment or pinned package version.

Risk: Prompts sent to the local router may be processed by other machines in the configured RTX fleet.

Mitigation: Use only trusted fleet machines and avoid sending sensitive prompts unless the fleet configuration and data-handling policy allow it.

Risk: Ollama service and environment changes persist after the setup steps are run.

Mitigation: Record the changes, review them before applying, and undo or reset them when the local AI server configuration is no longer needed.

Risk: Large model downloads and model deletion operations can affect disk usage and local model availability.

Mitigation: Require explicit confirmation before pulling or deleting models and avoid deleting or modifying files in `~/.fleet-manager/`.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/skills/rtx-local-ai)
- [Ollama Herd GitHub Repository](https://github.com/geeks-accelerator/ollama-herd)
- [Ollama Herd PyPI Package](https://pypi.org/project/ollama-herd/)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, PowerShell, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup commands, API request examples, monitoring commands, and configuration guidance for Windows and Linux.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
