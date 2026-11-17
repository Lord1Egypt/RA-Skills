## Description:

Use when footage needs color correction, white-balance or exposure repair, Log-to-Rec.709 conversion, named creative looks, skin-tone review, or a portable .cube LUT for a cut-as-code delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whitetowerai](https://clawhub.ai/user/whitetowerai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video-production agents use this skill to assess source footage, generate corrected and creative color looks, choose a look with rationale, bake a portable .cube LUT, and apply it to delivery video while preserving audio sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted looks.json or grade-plan files can influence FFmpeg filter chains and output filenames.

Mitigation: Use locally authored or trusted grade specs, review filters and paths before execution, and run untrusted workflows in a sandbox.

Risk: Media-processing outputs may write to shared or sensitive directories or consume substantial compute on large videos.

Mitigation: Use dedicated project output directories, avoid sensitive paths, and apply resource limits or faster preview presets before final rendering.

Risk: Automatic representative-frame and skin-crop heuristics may miss faces or changing lighting, producing misleading color decisions.

Mitigation: Review the generated contact sheet and skin-tone check, force a known face frame or crop when needed, and keep the final look selection rationale in the grade plan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whitetowerai/skills/video-color-grade)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, files]

**Output Format:** [Markdown guidance with JSON configuration, shell commands, review images, video files, and .cube LUT files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg/ffprobe and Python with numpy and Pillow; media outputs are written to user-selected project directories.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
