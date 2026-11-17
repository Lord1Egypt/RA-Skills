## Description:

Render TikTok-style animated pill captions onto short-form videos from an MP4, captions JSON, and optional background audio using MoviePy and PIL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:


## Use Case:

Developers and video automation users use this skill to create short-form social video caption overlays from structured JSON without manual editing in a video editor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented command installs unpinned MoviePy and Pillow packages at run time.

Mitigation: Run the skill in a locked environment and pin MoviePy and Pillow versions before production use.

Risk: The output path is user supplied and could overwrite an existing local file.

Mitigation: Choose a dedicated output path and check for existing files before rendering.

Risk: The bundled example captions include audience-specific advertising copy.

Mitigation: Review and replace the sample captions with copy appropriate for the intended audience and geography.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-video-caption-overlay)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown instructions with bash commands and JSON caption configuration; generated outputs are MP4 video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local video input, captions JSON, uv, MoviePy, Pillow, and optional audio or font files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
