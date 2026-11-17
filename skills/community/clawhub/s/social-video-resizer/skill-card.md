## Description:

Converts one social video into platform-ready size variants by choosing crop, pad, or proportional scale strategies for 9:16, 1:1, 4:5, and 16:9 while protecting faces, products, subtitles, and platform safe zones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Social media operators, marketers, and video production teams use this skill to plan platform-specific video resizing deliverables. It helps select crop, pad, or scale strategies, document tradeoffs, flag subtitle and safe-zone risks, and provide optional ffmpeg commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated ffmpeg commands may be incorrect for a specific source file or could affect important originals if run without review.

Mitigation: Review command parameters, work on copies, and confirm crop coordinates, codecs, and output paths before execution.

Risk: Platform dimensions, time limits, file-size limits, and safe zones can change after the bundled reference material is published.

Mitigation: Verify current platform or ad-backend requirements before final export and publishing.

Risk: The workflow is written in Chinese, which may lead to misapplication by users who cannot reliably read the guidance.

Mitigation: Use the skill only with users or reviewers who can understand the source guidance, or translate and review the plan before acting.

## Reference(s):

- [Output Template](references/output-template.md)
- [Platform Specification Sheet](references/platform-spec-sheet.md)
- [Crop / Pad / Scale Guide](references/crop-pad-scale-guide.md)
- [Resize Checklist](assets/resize-checklist.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown resizing plan with tables, risk notes, and optional ffmpeg command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and platform limits require human review before publishing or execution.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
