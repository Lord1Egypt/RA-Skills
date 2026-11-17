## Description:

Video Processor helps agents assist with video format conversion, compression, simple trimming, subtitle addition, and cover extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate or follow video-processing commands for common tasks such as format conversion, compression, simple edits, subtitle insertion, and cover extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install instructions execute a mutable latest-version npm package.

Mitigation: Review the install command before use, prefer a pinned and verified ClawHub installer version, and avoid elevated privileges.

Risk: Large video files may process slowly and consume temporary storage.

Mitigation: Check available storage before processing large files and set practical file-size or runtime limits for automated use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/skills/xiaoming-video-processor)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local video-processing tooling such as ffmpeg; large files may need adequate temporary storage.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
