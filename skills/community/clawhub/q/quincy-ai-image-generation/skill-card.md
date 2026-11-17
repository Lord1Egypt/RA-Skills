## Description:

AI Image Generation helps agents generate and edit images with 50+ models through SkillBoss API Hub, including text-to-image, image-to-image, inpainting, LoRA workflows, upscaling, and text rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, marketers, and content teams use this skill to have an agent call SkillBoss API Hub for image generation, image editing, upscaling, and model discovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts, generation settings, and provided image URLs are sent to SkillBoss API Hub.

Mitigation: Use only approved prompts and assets; avoid secrets, private images, regulated data, or confidential business material unless your organization permits that provider and data flow.

Risk: The skill requires a SkillBoss API key for API access.

Mitigation: Provide SKILLBOSS_API_KEY through an approved secret or environment-variable mechanism and avoid hard-coding it in prompts, files, or shared logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quincygunter/skills/quincy-ai-image-generation)
- [SkillBoss API Hub](https://api.heybossai.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, API calls, Configuration guidance]

**Output Format:** [Markdown with Python code blocks and returned image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; prompts, generation settings, and provided image URLs are sent to SkillBoss API Hub.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
