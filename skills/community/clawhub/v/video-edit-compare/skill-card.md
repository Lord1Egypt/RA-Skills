## Description:

Use when a completed cut-as-code delivery needs a strict side-by-side review against its original source, including cuts, varispeed, color grade, and graphics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whitetowerai](https://clawhub.ai/user/whitetowerai)

### License/Terms of Use:

MIT-0

## Use Case:

Video editors, reviewers, and media automation engineers use this skill to render a source-clock side-by-side comparison of an original video and final delivery. The review helps inspect cuts, dropped ranges, varispeed, color grade, graphics, and original-audio continuity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs media-processing commands that read selected source and final videos and write review artifacts.

Mitigation: Run it only in a trusted workspace and provide explicit project paths rather than a broad sensitive directory.

Risk: The workflow depends on local ffmpeg/ffprobe, Pillow, and video-understand/projectlib behavior.

Mitigation: Confirm these dependencies are installed from trusted sources before processing media.

Risk: Reordered, duplicated, overlapping, nonlinear-speed, or multi-source timelines are unsupported.

Mitigation: Use chronological, non-overlapping, single-source timelines and rely on the skill's validation failures before accepting a comparison.

## Reference(s):

- [Video Edit Compare on ClawHub](https://clawhub.ai/whitetowerai/skills/video-edit-compare)
- [WhiteTowerAI publisher profile](https://clawhub.ai/user/whitetowerai)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Video files]

**Output Format:** [MP4 comparison video, JSON compare plan, Markdown summary, and generated ffmpeg filtergraph]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg/ffprobe, Python, Pillow, and a trusted local projectlib dependency; validates duration, dimensions, dropped ranges, kept frames, and audio continuity after rendering.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
