## Description:

Generate RedNote image series with structured style and layout choices and bundled generation tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[632657122](https://clawhub.ai/user/632657122)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to plan and generate RedNote card series, cover cards, and social infographic sequences from a topic or outline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses IMAGE_GEN_API_KEY and can persist it in local configuration.

Mitigation: Use a limited WeryAI key, avoid persisting it unless plaintext local storage is acceptable, and never commit generated configuration containing secrets.

Risk: Generated batch references and broad local-reference handling can expose files or unintended inputs.

Mitigation: Inspect generated batch ref paths before running generation and use public HTTPS reference images when image references are needed.

Risk: Some commands rely on unpinned npx execution.

Mitigation: Run the skill in a controlled environment and review the generated commands before execution.

## Reference(s):

- [RedNote Dimensions Reference](references/dimensions.md)
- [RedNote Outline Template](references/outline-template.md)
- [RedNote Presets](references/presets.md)
- [RedNote Prompt Template](references/prompt-template.md)
- [WeryAI Text-to-Image API](https://docs.weryai.com/api-reference/image-generation/submit-text-to-image-task)
- [WeryAI Image-to-Image API](https://docs.weryai.com/api-reference/image-generation/submit-image-to-image-task)
- [Rednote Images on ClawHub](https://clawhub.ai/632657122/skills/rednote-images)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Image files]

**Output Format:** [Markdown outlines and prompts, JSON batch files, shell commands, local configuration, and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMAGE_GEN_API_KEY, Node.js, npm, and either bun or npx; may write output images and optional local .image-skills configuration.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
