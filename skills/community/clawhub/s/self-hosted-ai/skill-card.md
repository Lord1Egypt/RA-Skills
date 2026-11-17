## Description:

Self Hosted Ai helps agents guide users through running self-hosted LLM inference, image generation, speech-to-text, embeddings, and local fleet routing without cloud APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twinsgeeks](https://clawhub.ai/user/twinsgeeks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install, run, and query a self-hosted AI router across macOS, Linux, and Windows machines for local LLM, image, transcription, and embedding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package and tool installation steps can affect the user's local environment.

Mitigation: Verify the referenced packages before installation and prefer an isolated virtual environment or tool environment.

Risk: herd-node performs local-network discovery.

Mitigation: Run the service only on trusted networks and review router or node exposure before use.

Risk: Prompts, audio, and documents are processed by the local service the user runs.

Mitigation: Confirm that the local service, models, and host machines are appropriate for the sensitivity of the data being processed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/twinsgeeks/skills/self-hosted-ai)
- [Ollama Herd repository](https://github.com/geeks-accelerator/ollama-herd)
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md)
- [Image Generation Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/image-generation.md)
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md)
- [Configuration Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/configuration-reference.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, API calls, configuration]

**Output Format:** [Markdown with inline bash, Python, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local service endpoints and user-managed local model tooling.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
