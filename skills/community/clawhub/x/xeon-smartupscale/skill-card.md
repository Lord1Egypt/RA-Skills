## Description:

Xeon Smartupscale helps agents upscale videos to target resolutions using Lanczos pre-scaling and an ETDS 2x OpenVINO model on Intel Xeon CPUs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wray151](https://clawhub.ai/user/wray151)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to upscale generated or legacy videos to targets such as 1080p, 1440p, and 4K on Linux x86_64 systems with Intel CPU acceleration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads and installs remote executable dependencies without integrity checks.

Mitigation: Review install.sh before execution, prefer a system ffmpeg, avoid elevated privileges, and install only if unverified remote dependency downloads are acceptable.

Risk: Video conversion commands can overwrite existing output files.

Mitigation: Check output paths before running the skill and use explicit -o paths that do not point to important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wray151/skills/xeon-smartupscale)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files]

**Output Format:** [Markdown with inline bash commands and generated MP4 video file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs H.264 MP4 video with CRF 18 and merged audio when present; explicit output paths should be checked because existing files may be overwritten.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
