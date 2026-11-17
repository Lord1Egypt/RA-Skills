## Description:

Generates visual assets such as posters, social media images, video covers, and virtual-human backgrounds by turning user requirements into image prompts and optional image-generation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and agents use this skill to convert visual-content requests into structured image prompts, generation commands, platform size choices, and local image outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud image generation sends prompts to OpenAI when DALL-E 3 is selected.

Mitigation: Prefer the local Stable Diffusion path for sensitive prompts and use DALL-E 3 only when the user accepts external API processing.

Risk: Generated text inside images can be distorted or inaccurate.

Mitigation: Review generated images before publication and use manual layout or post-processing for exact typography.

Risk: Optional Feishu upload can move generated assets to cloud storage.

Mitigation: Upload only after an explicit user-selected action and avoid uploading sensitive images without approval.

Risk: Some advertised generation backends or post-processing capabilities may be incomplete.

Mitigation: Confirm the selected engine and dependencies are available before relying on the workflow for production output.

Risk: Commercial use can raise rights or licensing questions for generated imagery.

Mitigation: Check generated assets and model terms before commercial publication.

## Reference(s):

- [Visual Style Guide](references/visual-style-guide.md)
- [Prompt Template Library](references/prompt-templates.md)
- [Platform Size Guide](references/platform-size-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/tujinsama/skills/visual-content-generator-claw)
- [Publisher Profile](https://clawhub.ai/user/tujinsama)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON status output from the generation script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local PNG files when an available image-generation backend is configured.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
