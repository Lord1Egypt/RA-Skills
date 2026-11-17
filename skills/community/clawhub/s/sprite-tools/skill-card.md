## Description:

Sprite Tools helps agents split generated sprite sheets into individual sprites and trim transparent or fixed-color backgrounds for PNG, JPG, and WebP assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical artists, and game teams use this skill to turn generated sprite-sheet images into individual asset files and clean up simple transparent or solid-color backgrounds. It is useful for preparing image assets for downstream game, art, or prototyping workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing dependencies directly into a system Python environment can affect other Python tooling.

Mitigation: Install Pillow, numpy, and optional rembg dependencies in a virtual environment.

Risk: Optional system package installation can require elevated privileges.

Mitigation: Avoid the optional sudo-based ImageMagick install unless a reviewer confirms it is needed for the intended environment.

Risk: Using the optional remove.bg API can upload private or proprietary images to a third-party service and requires protecting an API key.

Mitigation: Use local scripts for sensitive images and treat any remove.bg API key as a secret.

## Reference(s):

- [ClawHub Sprite Tools release page](https://clawhub.ai/axelhu/skills/sprite-tools)
- [ClawHub publisher profile: axelhu](https://clawhub.ai/user/axelhu)
- [remove.bg API endpoint referenced by the skill](https://api.remove.bg/v1.0/removebg)

## Skill Output:

**Output Type(s):** [shell commands, guidance, code, files]

**Output Format:** [Markdown guidance with inline shell and Python commands; scripts produce image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected image inputs are PNG, JPG, or WebP files; generated sprite outputs are typically numbered PNG files in a chosen output directory.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
