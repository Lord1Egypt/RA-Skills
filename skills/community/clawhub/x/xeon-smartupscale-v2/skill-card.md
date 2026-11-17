## Description:

Generic Xeon-CPU video upscaler that plans Lanczos pre-scaling plus Real-ESRGAN general-x4v3 x4 passes to reach a target resolution, with super-resolution always last and a 270-line pre-scale floor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wray151](https://clawhub.ai/user/wray151)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video-processing users can use this skill to upscale video files on Linux x86_64 systems with a planned Lanczos and OpenVINO Real-ESRGAN CPU pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer may run mutable third-party bootstrap code and unverified native binaries with the user's privileges.

Mitigation: Review install.sh before use, avoid running it as root, use an isolated environment, and prefer trusted system packages for pip, ffmpeg, and ffprobe.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wray151/skills/xeon-smartupscale-v2)
- [ffmpeg static build download used by installer](https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz)
- [pip bootstrap script used by installer](https://bootstrap.pypa.io/get-pip.py)

## Skill Output:

**Output Type(s):** [shell commands, guidance, files]

**Output Format:** [Markdown guidance with shell commands; execution produces H.264 MP4 video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets include common resolution presets and explicit WxH dimensions; audio is copied when present.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
