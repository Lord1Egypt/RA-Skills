## Description:

Generates images through a locally running SGLang-Diffusion server using its OpenAI-compatible image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangyukunok](https://clawhub.ai/user/jiangyukunok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and image-generation users use this skill to ask an agent to create PNG images through a configured local SGLang-Diffusion server, with optional prompt, size, seed, denoising, guidance, output path, and API-key settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send prompts and optional API credentials to a user-selected SGLang-Diffusion server.

Mitigation: Prefer the default localhost server or HTTPS for remote servers, and provide real API keys through environment variables or protected configuration instead of command-line arguments.

Risk: The skill depends on an external local or remote image-generation service being available and compatible with the OpenAI-style images endpoint.

Mitigation: Confirm the SGLang-Diffusion server is running and reachable before invoking the generator.

## Reference(s):

- [SGLang project](https://github.com/sgl-project/sglang)
- [ClawHub skill page](https://clawhub.ai/jiangyukunok/skills/sglang-diffusion)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance and shell commands; generated image output is saved as a PNG file path with a MEDIA line.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a reachable SGLang-Diffusion server; defaults to localhost and timestamped PNG output in /tmp/.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
