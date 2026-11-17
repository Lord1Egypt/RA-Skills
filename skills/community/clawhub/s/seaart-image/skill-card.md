## Description:

Use this skill to generate AI images using the SeaArt platform (seaart.ai). Supports text-to-image generation with multiple models, custom dimensions, LoRA models, and negative prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seaartpublic](https://clawhub.ai/user/seaartpublic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate SeaArt text-to-image results from prompts, model choices, dimensions, negative prompts, and optional LoRA settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructions can expose the SeaArt authentication token in logs.

Mitigation: Use a non-printing token presence check and never print, paste, or log the SEAART_TOKEN value.

Risk: Prompts, generation settings, and the SeaArt session token are sent to SeaArt to generate images.

Mitigation: Use the skill only when the user trusts SeaArt with the prompt content and account session token.

Risk: The skill may require installing the Python requests dependency.

Mitigation: Install dependencies from a trusted source, preferably in a virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seaartpublic/skills/seaart-image)
- [Publisher profile](https://clawhub.ai/user/seaartpublic)
- [SeaArt platform](https://www.seaart.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SeaArt generation status, cost information, content-review filtering notes, and one or more generated image URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
