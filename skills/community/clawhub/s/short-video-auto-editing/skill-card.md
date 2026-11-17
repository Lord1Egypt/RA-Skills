## Description:

Automates short-form video mashup production with MoviePy-based media selection and editing, Edge TTS voiceover generation, subtitle synchronization, quality checks, and batch output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dally-bee](https://clawhub.ai/user/dally-bee)

### License/Terms of Use:

MIT-0

## Use Case:

Social media operators, creators, and developers use this skill to generate batches of 15-20 second vertical promotional videos for platforms such as Douyin, WeChat Channels, and Xiaohongshu. It is intended for workflows that combine local video materials, marketing copy, AI voiceover, subtitles, quality checks, and repeated variant generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketing copy submitted for voiceover may be handled by Edge TTS rather than staying entirely local.

Mitigation: Use only copy you are comfortable processing with Edge TTS, and avoid sensitive unpublished customer or business text unless that handling is acceptable.

Risk: Batch generation writes multiple media outputs and may target the wrong path if configuration is not checked.

Mitigation: Confirm output paths before batch runs and keep generated videos in the documented output directory.

Risk: Generated promotional videos can repeat source materials or fail platform-ready quality checks.

Mitigation: Maintain a sufficiently large source-material library and run the documented checks for duration, resolution, frame rate, audio presence, file size, and repetition.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dally-bee/skills/short-video-auto-editing)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [markdown, code, configuration, guidance]

**Output Format:** [Markdown with Python code blocks, workflow steps, configuration examples, and quality-control guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets batch generation of 15-20 second 1080x1920 short videos using MoviePy media processing and Edge TTS voice rotation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
