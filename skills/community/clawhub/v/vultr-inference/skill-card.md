## Description:

Generate images and text using Vultr Inference API. Supports Flux image generation and various LLMs for text. Use when user wants to generate images, artwork, or text completions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happytreees](https://clawhub.ai/user/happytreees)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to generate images and text completions through Vultr Inference, list available models, and troubleshoot API requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and chat messages are sent to Vultr through the Inference API.

Mitigation: Avoid sending sensitive prompts or messages unless the use case and Vultr account controls permit it.

Risk: The skill uses a Vultr API key stored in local configuration.

Mitigation: Prefer an inference-only, least-privileged key if available and keep ~/.config/vultr/api_key private.

Risk: The helper script downloads remote image output and supports custom output paths.

Mitigation: Review the script and requested output path before running image downloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/happytreees/skills/vultr-inference)
- [Vultr Inference API base endpoint](https://api.vultrinference.com/v1)
- [Vultr image generation endpoint](https://api.vultrinference.com/v1/images/generations)
- [Vultr chat completions endpoint](https://api.vultrinference.com/v1/chat/completions)
- [Vultr models endpoint](https://api.vultrinference.com/v1/models)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, image files]

**Output Format:** [Markdown guidance with bash, Python, and JSON examples; the helper script prints model lists and can save PNG image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Vultr API key file at ~/.config/vultr/api_key and network access to Vultr Inference API.]

## Skill Version(s):

1.1.2 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
