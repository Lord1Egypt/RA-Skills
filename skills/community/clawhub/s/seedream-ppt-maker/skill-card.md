## Description:

Creates image-based PowerPoint decks from Markdown content using the Baoyu layout framework and Seedream 5.0, with an optional step-by-step confirmation workflow to reduce revisions and API quota use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindypapa](https://clawhub.ai/user/cindypapa)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn structured Markdown content into image-based PPT presentations. It can recommend layout and style combinations, preview prompts, call Seedream image generation, and assemble generated images into a PowerPoint file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation content can be sent to Volces/Seedream during image generation.

Mitigation: Avoid confidential or regulated content unless the user accepts third-party processing by that service.

Risk: Seedream calls use the configured API key and can consume paid quota.

Mitigation: Use the interactive confirmation flow to review layout, style, and prompts before generation.

Risk: The install checker prints a prefix of the stored API key.

Mitigation: Remove key-prefix logging or avoid running the checker in shared, recorded, or captured terminals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cindypapa/skills/seedream-ppt-maker)
- [Source homepage](https://github.com/Cindypapa/baoyu-seedream-ppt)
- [Baoyu layout system](https://github.com/JimLiu/baoyu-skills)
- [Volcengine](https://www.volcengine.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and generated file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated project folders may contain config.json, prompt text files, PNG images, and a PPTX presentation.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
