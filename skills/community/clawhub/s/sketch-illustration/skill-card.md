## Description:

Generates hand-drawn illustration prompts and images in multiple styles for flowcharts, product explainers, PPT visuals, tutorials, knowledge diagrams, and infographics, then can send generated images to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dadaniya99](https://clawhub.ai/user/dadaniya99)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan, prompt, generate, iterate, and optionally deliver Chinese-labeled hand-drawn illustrations for presentations, tutorials, product explanations, knowledge posters, and information graphics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated images and prompts may leave the local environment through configured image generation services.

Mitigation: Use the skill only when external image generation is intended, and avoid sending sensitive or confidential content in prompts.

Risk: The Feishu send path uses local app credentials and includes a hard-coded default recipient.

Mitigation: Verify the recipient for every send, remove the default open_id before deployment, and grant only scoped Feishu credentials to a trusted sender.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dadaniya99/skills/sketch-illustration)
- [Style options](artifact/references/styles.md)
- [Prompt guide](artifact/references/prompt-guide.md)
- [Image assistant workflow](artifact/references/image-assistant-workflow.md)
- [API configuration](artifact/references/api-config.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with prompt blocks, command examples, and generated image files when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation can use configured external image APIs and Feishu delivery credentials.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
