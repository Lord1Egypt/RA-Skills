## Description:

Generate, vectorize, upscale, replace background, variate, remove background, and transform images via Recraft API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nkrcrft](https://clawhub.ai/user/nkrcrft)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to create, edit, upscale, vectorize, and transform images through the Recraft API from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and selected input images to Recraft using a Recraft API token.

Mitigation: Install and run it only when sharing those prompts, images, and token-scoped API access with Recraft is acceptable.

Risk: The user-info command can print account details such as email and credits into the session transcript or logs.

Mitigation: Run user-info only when that account information is intended to be visible in the current agent session.

## Reference(s):

- [Recraft](https://www.recraft.ai/)
- [Recraft API profile](https://www.recraft.ai/profile/api)
- [Recraft AI on ClawHub](https://clawhub.ai/nkrcrft/skills/recraft)
- [Publisher profile](https://clawhub.ai/user/nkrcrft)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command examples and generated image or SVG file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves generated or transformed media files and prints MEDIA lines where supported.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
