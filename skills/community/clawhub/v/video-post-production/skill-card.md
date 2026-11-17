## Description:

End-to-end short-video post-production from one raw talking-head video: transcribe speech, build timed subtitle phrases, highlight key words, place sound effects (SFX), choose background music (BGM), and render a polished final video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiepige8](https://clawhub.ai/user/tiepige8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video creators use this skill to turn a single spoken raw video into a short-form edited video with timed subtitles, meaningful keyword highlights, optional SFX, optional BGM, and a rendered MP4 export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted production plans may cause weak path validation to pull SFX audio from outside the intended SFX folder.

Mitigation: Install only from trusted sources, keep inputs and outputs in a dedicated workspace, avoid arbitrary SFX type values, and review production_plan.json before rendering.

Risk: FFmpeg and Python media tooling can overwrite files or process untrusted media inputs locally.

Mitigation: Run the workflow in a virtual environment with pinned dependencies and review generated subtitles, output paths, and publish-ready media before release.

## Reference(s):

- [ASS Subtitle Effects Reference](references/ass_effects.md)
- [Audio Resources and Douyin Ad Audio Design Guide](references/audio_resources.md)
- [Mixkit Commercial Music](https://mixkit.co/free-stock-music/tag/commercial/)
- [Mixkit Whoosh Sound Effects](https://mixkit.co/free-sound-effects/whoosh/)
- [Pixabay Music](https://pixabay.com/music/)
- [Incompetech](https://incompetech.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, JSON production plans, ASS subtitle files, and MP4 video outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a video-specific output directory containing alignment.json, production_plan.json, subtitles.ass, and final.mp4 when the workflow is executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
