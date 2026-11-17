## Description:

Generate and stitch short MP4 video clips from text prompts and optional reference images using Google Veo 3.x via the Gemini API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to generate short video clips from prompts, create longer videos by stitching multiple generated segments, and guide generation with style or product reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference images are sent to Google's Gemini/Veo API.

Mitigation: Avoid sensitive prompts or reference images, and use a private output directory for generated media.

Risk: API keys may be exposed if passed directly on the command line.

Mitigation: Prefer GEMINI_API_KEY, use a restricted key, and avoid passing secrets through shell history.

Risk: Dependency setup and ffmpeg path handling need review before use.

Mitigation: Review or pin Python dependencies and run a trusted ffmpeg binary from a known PATH.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-veo3-video-gen)
- [zero2ai-hub publisher profile](https://clawhub.ai/user/zero2ai-hub)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, code]

**Output Format:** [Markdown with inline bash code blocks and CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script can save MP4 files and print MEDIA paths when generation succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
