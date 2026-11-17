## Description:

Ubuntu Ai helps agents set up and operate a local AI platform on Ubuntu or Debian using Ollama Herd for LLM inference, image generation, embeddings, and heterogeneous CPU, GPU, and ARM clusters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and configure a local Ubuntu or Debian AI stack, including Ollama Herd routing, node registration, systemd services, CUDA checks, API examples, and monitoring commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run unverified installers and create persistent network services that may run with elevated privileges.

Mitigation: Review and harden the installation before use; prefer verified or packaged Ollama installation, pin and verify ollama-herd, use a virtual environment, and run router or node services as an unprivileged user or foreground process where possible.

Risk: The skill exposes an AI router on port 11435.

Mitigation: Avoid opening port 11435 broadly; restrict access to specific trusted hosts or a private network.

## Reference(s):

- [Ubuntu Ai ClawHub skill page](https://clawhub.ai/twinsgeeks/skills/ubuntu-ai)
- [Ollama Herd repository](https://github.com/geeks-accelerator/ollama-herd)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with bash, Python, and HTTP API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Linux-focused; requires curl or wget and may use python3, pip, nvidia-smi, systemctl, and apt.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
