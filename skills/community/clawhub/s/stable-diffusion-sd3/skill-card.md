## Description:

Stable Diffusion 3 and SD3.5 Large on Apple Silicon - generate Stable Diffusion images locally with DiffusionKit's MLX-native backend, with Flux models via mflux and Ollama native image generation routed across a local device fleet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up and operate local Stable Diffusion, Flux, and related model workflows on Apple Silicon fleets through shell commands, API examples, and configuration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to install PyPI and uv packages and run a local fleet router.

Mitigation: Install in an isolated environment and verify that referenced packages and the local router are trusted before use.

Risk: The skill references a macOS compatibility patch script.

Mitigation: Review the script source before running it and only execute it when the compatibility patch is needed.

Risk: Optional LLM, transcription, and embedding endpoints expand the local service surface beyond image generation.

Mitigation: Enable or call those endpoints only with explicit user intent and appropriate local access controls.

## Reference(s):

- [Stable Diffusion Sd3 on ClawHub](https://clawhub.ai/twinsgeeks/skills/stable-diffusion-sd3)
- [Ollama Herd Homepage](https://github.com/geeks-accelerator/ollama-herd)
- [Image Generation Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/image-generation.md)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, Python, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing setup steps, API examples, monitoring commands, and operational guardrails; it does not directly generate images by itself.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
