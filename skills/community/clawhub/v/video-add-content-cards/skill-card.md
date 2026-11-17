## Description:

Use when an understood video project needs selective transcript-timed titles, lower-thirds, statistics, metric spotlights, comparisons, lists, quotes, chapter cards, or calls to action authored as HyperFrames HTML graphics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whitetowerai](https://clawhub.ai/user/whitetowerai)

### License/Terms of Use:

MIT-0

## Use Case:

Video editors and developers use this skill to turn reviewed transcript moments into approved, timed content cards and transparent graphics overlays while keeping captions and important faces clear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the workflow reads and writes files in the video project.

Mitigation: Use only with trusted projects and review generated plans and assets before approving them.

Risk: Local HTML previews may make browser network requests, and rendering depends on external tools and packages.

Mitigation: Open previews in a trusted environment and check ffmpeg, Node.js, HyperFrames, and browser availability before rendering.

Risk: Inaccurate card copy or placement can misrepresent evidence or obscure faces and captions.

Mitigation: Check claims against reviewed source evidence and approve composited stills and motion windows before the final overlay.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/whitetowerai/skills/video-add-content-cards)
- [Content Card Chart Data](artifact/reference/chart-data.md)
- [Content Card Review Design](artifact/reference/ux-design.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Files, Configuration, Shell commands]

**Output Format:** [Markdown guidance, JSON card plans, HTML graphics, and transparent video overlays]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses reviewed video evidence and human approval before rendering selected cards.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
