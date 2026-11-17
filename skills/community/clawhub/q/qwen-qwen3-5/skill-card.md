## Description:

Run Qwen 3.5, Qwen3-Coder, and Qwen3-ASR across a local device fleet through Ollama Herd.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and operate Ollama Herd so local machines can route Qwen model requests for reasoning, coding, speech transcription, image generation, embeddings, and fleet monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to install and run an unpinned PyPI package.

Mitigation: Install only if the ollama-herd package and repository are trusted; prefer a virtual environment and pin a reviewed version when possible.

Risk: Prompts, audio files, generated outputs, logs, and model activity may pass through the local fleet service.

Mitigation: Run the router and nodes only on trusted devices and trusted networks.

## Reference(s):

- [Ollama Herd PyPI Package](https://pypi.org/project/ollama-herd/)
- [Ollama Herd Repository](https://github.com/geeks-accelerator/ollama-herd)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, Python, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup commands, local API examples, hardware recommendations, monitoring commands, and guardrails.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
