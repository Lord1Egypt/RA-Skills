## Description:

WSL2 Local AI helps Windows developers run local LLM workflows through WSL2 with NVIDIA GPU passthrough, Ollama, CUDA, Docker, and Ollama Herd routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up and operate a Windows plus WSL2 local AI stack, including Ollama installation, WSL2 GPU verification, Ollama Herd routing, Docker workflows, local API calls, image generation, and embeddings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup commands may execute mutable remote installers or install unpinned packages.

Mitigation: Review commands before execution, download installers for inspection, verify checksums or signatures where available, and pin package versions.

Risk: Container setup may use an unpinned image tag.

Mitigation: Use a tagged or digest-pinned Docker image and review the image source before running GPU-enabled containers.

Risk: The setup changes the WSL2 environment and may start long-running local services.

Mitigation: Run commands in a controlled WSL2 environment, confirm service ports before exposing them, and keep local API endpoints bound only as intended.

Risk: Local model downloads and deletions can affect disk usage or remove user-selected assets.

Mitigation: Require explicit confirmation for model pulls and deletions, consistent with the skill's stated guardrails.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/twinsgeeks/skills/wsl2-local-ai)
- [Ollama Herd repository](https://github.com/geeks-accelerator/ollama-herd)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with PowerShell, bash, Python, JSON, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Windows and WSL2 setup steps, local service endpoints, hardware guidance, and guardrails for model download and deletion confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
