## Description:

Free AI text-to-image generation that turns text descriptions into images without an API key and supports multiple Pollinations.ai models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bustes01](https://clawhub.ai/user/bustes01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to generate image files from text prompts with optional size, seed, and model parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt text is sent to Pollinations.ai.

Mitigation: Do not use sensitive, confidential, or regulated prompts with this skill.

Risk: The documented command pattern can execute crafted prompt text as local Python code.

Mitigation: Pass prompts as data to the URL-encoding step instead of interpolating them into python3 -c source.

Risk: The documented output path is a fixed temporary file.

Mitigation: Write generated images to a unique private temporary path before returning them to the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bustes01/skills/text-to-image-free)
- [ClawHub metadata homepage](https://clawhub.ai/BusTes01/text-to-image-free)
- [Pollinations.ai image endpoint](https://image.pollinations.ai/prompt/{prompt})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports width, height, model, nologo, and seed parameters; generated images are written as local files.]

## Skill Version(s):

1.3.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
