## Description:

Expands short Chinese keywords or reference-image requests into detailed whiteboard illustration prompts and invokes image_synthesize to generate tightly cropped whiteboard images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and business users use this skill to turn brief Chinese topic ideas into reusable English prompts and generated whiteboard-style illustration images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts can include confidential ideas and are sent to an image generation workflow and then through Feishu.

Mitigation: Review prompts before generation and avoid submitting confidential or sensitive content unless that sharing path is approved.

Risk: Generated Chinese text in the image may be imprecise or unsuitable for publication.

Mitigation: Review generated images before reuse and add precise final text in an editing tool when accuracy matters.

## Reference(s):

- [Whiteboard Prompt Template Library](references/prompt-library.md)
- [Extended Icon Guide](references/icon-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Generated image file plus prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a PNG file under /workspace and send the generated image and prompt text to the user.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
