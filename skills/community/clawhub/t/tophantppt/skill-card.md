## Description:

Generates image-based PPTX presentation decks from specified slide content or source material using fixed background reference images for visual consistency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizhedm](https://clawhub.ai/user/lizhedm)

### License/Terms of Use:

MIT-0

## Use Case:

Presentation creators and agents use this skill to turn user-provided slide outlines or raw source material into visually consistent, full-image PowerPoint decks. It is suited to producing slide images and assembling them into a PPTX when editability of individual text elements is not required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches fixed background reference images from GitHub and may retry when retrieval fails, which can affect reliability and disclose usage context in restricted environments.

Mitigation: Use in environments where remote image retrieval and image-generation workflows are permitted, and review or cache required reference images before offline or privacy-sensitive use.

Risk: Generated slides are image-based, so text and visual details may be inaccurate or difficult to edit after generation.

Mitigation: Review generated slide images for content accuracy, readability, and layout before sharing the final PPTX.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lizhedm/skills/tophantppt)
- [Publisher profile](https://clawhub.ai/user/lizhedm)
- [Skill homepage](https://clawic.com/skills/tophantppt)

## Skill Output:

**Output Type(s):** [Markdown, Files, Code, Shell commands, Guidance]

**Output Format:** [Markdown instructions and generated PPTX/image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces full-image 16:9 slides, typically at 1920x1080 or higher, and merges them into a PPTX.]

## Skill Version(s):

1.0.4 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
