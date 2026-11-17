## Description:

Adds word-timed captions to an Open Recut program using its canonical transcript and timeline, with style review and a transparent overlay for delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whitetowerai](https://clawhub.ai/user/whitetowerai)

### License/Terms of Use:

MIT-0

## Use Case:

Video editors and developers use this skill to turn a validated, word-level transcript into timeline-aligned captions, review their appearance, and add a caption overlay to an Open Recut delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local media processing can read and generate project files.

Mitigation: Use only with projects that expect local media processing and keep the working directory project-scoped.

Risk: Caption layout or timing may not match the intended delivery.

Mitigation: Review the generated HTML evidence and source-backed preview before approval.

Risk: On-demand HyperFrames resolution can introduce an unpinned dependency.

Mitigation: Consider pinning HyperFrames rather than relying on ambient npx resolution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/whitetowerai/skills/video-add-captions)
- [Caption rules and data shape](reference/caption-rules.md)
- [Caption style themes](reference/caption-style-themes.md)
- [Caption feedback mapping](reference/caption-feedback-mapping.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Guidance, Shell commands]

**Output Format:** [Caption plan and review evidence in JSON, subtitles in SRT, review in HTML and Markdown, and a transparent PNG overlay sequence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Caption timing follows the canonical program timeline; review and approval precede delivery registration.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
