## Description:

Generate images from text prompts using xAI's Grok API with options for output format, batch size, and OpenClaw media attachment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mexicanamerican](https://clawhub.ai/user/mexicanamerican)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to ask an agent to create images through xAI's image generation API, save generated media, or return base64 output for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generated-image requests are sent to xAI using the user's xAI API key.

Mitigation: Use the skill only for prompts suitable for xAI processing and review xAI account, billing, and data-handling expectations before deployment.

Risk: The xAI API key could be exposed through shared dotfiles, synced shell profiles, logs, or copied setup snippets.

Mitigation: Prefer a per-session export or secret manager, and avoid storing the key in shared or synced shell configuration files.

Risk: The reviewed package appears to be missing the documented xai-gen executable.

Mitigation: Verify the executable is present and runnable before installation, publication, or agent use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mexicanamerican/skills/xai-image-gen)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Artifact README.md](artifact/README.md)
- [xAI console](https://console.x.ai)
- [xAI image generation endpoint](https://api.x.ai/v1/images/generations)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration guidance]

**Output Format:** [Image files with MEDIA path text, or base64 text; documentation uses Markdown with shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XAI_API_KEY; batch mode can produce multiple generated image files.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
