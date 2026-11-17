## Description:

Video Resize helps agents reformat videos to common platform aspect ratios with local ffmpeg center-crop resizing and points to an API-keyed AI Edit path for subject-aware cropping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[symbolk](https://clawhub.ai/user/symbolk)

### License/Terms of Use:


## Use Case:

Developers, creators, and agents use this skill to convert local videos to 9:16, 1:1, 16:9, 4:3, or 21:9 outputs for social and video platforms. Use the remote AI Edit path only when subject-aware reframing is required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented AI Edit path can upload selected videos and prompt data to an external service.

Mitigation: Use the local resize script by default; use AI Edit only with informed approval for sending media and prompt data to the external service.

Risk: The documented API-key check command can reveal a real SPARKI_API_KEY in output or logs.

Mitigation: Do not run that check as written; use non-revealing environment checks and rotate any key that was exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/symbolk/skills/video-resize)
- [Sparki homepage](https://sparki.io)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands; the resize script returns the resized video path on stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local resizing requires ffmpeg. The optional AI Edit path requires SPARKI_API_KEY and may send selected video and prompt data to an external service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
