## Description:

Xeonupscale resizes videos to higher resolutions with FFmpeg lanczos scaling, libx264 video encoding, and copied audio, with optional bundled static FFmpeg installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wray151](https://clawhub.ai/user/wray151)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video-processing users can use this skill to ask an agent to upscale local video files to standard presets or a custom WxH resolution using FFmpeg.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can fetch mutable remote code and execute a downloaded FFmpeg binary locally.

Mitigation: Review the installer first, clone a pinned commit or release, and verify the FFmpeg archive against a published checksum or signature before use.

Risk: The documented curl-to-bash installation path reduces reviewability before execution.

Mitigation: Avoid curl-to-bash installation; clone the repository, inspect the scripts, and run without elevated privileges.

Risk: Reinstallation can replace an existing xeonupscale skill directory.

Mitigation: Back up any existing xeonupscale skill directory before reinstalling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wray151/skills/xeonupscale)
- [BtbN FFmpeg Builds](https://github.com/BtbN/FFmpeg-Builds/releases/latest)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files]

**Output Format:** [Markdown guidance with bash command examples; generated MP4 video files from the shell script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses FFmpeg/libx264 with lanczos scaling; presets include 540p, 720p, 1080p, 1440p, and 2160p/4k.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
