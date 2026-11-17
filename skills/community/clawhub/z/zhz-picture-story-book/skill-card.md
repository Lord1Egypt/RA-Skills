## Description:

Creates illustrated picture stories with a separate caption on each page and a compiled PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjbook](https://clawhub.ai/user/bjbook)

### License/Terms of Use:

MIT-0

## Use Case:

Storytellers, educators, and creators use this skill to plan and produce illustrated picture books and sequential stories with readable captions and a PDF edition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation may add the Pillow dependency to the local Python environment.

Mitigation: Review dependencies and install in an isolated environment.

Risk: Creating illustrations requires a separately configured image-generation skill.

Mitigation: Confirm the image-generation tool is available before starting a story.

Risk: Generated prompts, images, logs, and PDFs are written to the working project directory; generated story content may be unsuitable or inaccurate.

Mitigation: Review the storyboard and prompts before image generation, and inspect the outputs before sharing.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bjbook/skills/zhz-picture-story-book)
- [Caption examples](references/caption-examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Images, PDF]

**Output Format:** [Markdown storyboards and prompts, PNG illustrated pages, and a PDF]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically 3–30 pages, with captions kept separate from the generated illustrations.]

## Skill Version(s):

1.0.1 (source: ClawHub release; skill frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
