## Description:

Designs, generates, quality-checks, uploads, and embeds AI illustrations such as architecture diagrams, flowcharts, infographics, and schematic images from article content and user prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gogoingai](https://clawhub.ai/user/gogoingai)

### License/Terms of Use:

MIT

## Use Case:

Developers, writers, and content teams use this skill to turn article image placeholders or direct drawing requests into structured image prompts, generated diagrams, quality checks, uploads, and embedded Markdown image references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented workflow can mishandle article-controlled prompt or path text while forming image-generation commands.

Mitigation: Use structured CLI arguments or carefully escaped prompt and path values, and avoid pasting untrusted article text directly into shell commands.

Risk: The skill uses local image-provider credentials and can upload generated images to a configured host.

Mitigation: Install only from a trusted publisher, verify the wenqu-cli package source before use, run the documented doctor check, and keep credential files owner-only.

Risk: The workflow can edit article files and replace embedded image references.

Mitigation: Review generated prompts, quality-check results, and file changes before accepting updates, especially when source article content is untrusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gogoingai/skills/wenqu-image)
- [Skill source homepage](https://github.com/gogoingai/wenqu-skills/tree/master/wenqu-image)
- [Project repository](https://github.com/gogoingai/wenqu-skills)
- [Image generation workflow](references/gen-workflow.md)
- [Core drawing principles](references/core-principles.md)
- [Diagram type selector](references/diagram-type-selector.md)
- [Design principles](references/design-principles.md)
- [Common pitfalls](references/pitfalls.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions, YAML-frontmatter prompt blocks, shell commands, configuration guidance, and image URL references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce generated-image metadata, CDN image URLs, and article file updates after user confirmation.]

## Skill Version(s):

0.1.19 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
