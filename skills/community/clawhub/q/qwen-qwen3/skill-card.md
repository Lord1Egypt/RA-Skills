## Description:

Qwen Qwen3 helps agents set up and use Qwen3.5, Qwen3, Qwen3-Coder, Qwen2.5-Coder, and Qwen3-ASR through a local Ollama Herd fleet for LLM inference, code generation, and speech-to-text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI practitioners use this skill to configure local Qwen model serving across macOS, Linux, and Windows fleets. It provides setup commands, API examples, and model-selection guidance for chat, code generation, and speech-to-text workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup commands install local packages and services that may affect the user's environment.

Mitigation: Use an isolated user environment, avoid administrator or root execution, and review or pin packages before installation when stricter supply-chain control is needed.

Risk: Prompts, audio, and generated-content requests may be routed across the configured local fleet.

Mitigation: Confirm which local machines participate in the fleet before sending sensitive content, and restrict fleet membership according to the deployment's privacy requirements.

Risk: Large Qwen models can exceed available device memory or consume substantial local resources.

Mitigation: Check available memory before model pulls and choose a smaller or MoE model variant when hardware is constrained.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/skills/qwen-qwen3)
- [Ollama Herd Repository](https://github.com/geeks-accelerator/ollama-herd)
- [Ollama Herd PyPI Package](https://pypi.org/project/ollama-herd/)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, and local API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local setup commands and model selection guidance; should not pull or delete Qwen models without user confirmation.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
