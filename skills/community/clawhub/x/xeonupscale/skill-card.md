## Description: <br>
Xeonupscale helps an agent upscale video files to preset or custom resolutions with ffmpeg's Lanczos scaler and libx264 encoding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wray151](https://clawhub.ai/user/wray151) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to upscale local video files to presets such as 540p, 1080p, or a custom WxH resolution while preserving audio when possible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install-time supply-chain exposure from downloading a static ffmpeg archive and supporting curl-to-bash installation. <br>
Mitigation: Install only after reviewing the repository and BtbN ffmpeg build source; prefer cloning and reviewing the files over curl-to-bash. <br>
Risk: Installing over an existing xeonupscale skill directory can discard local changes. <br>
Mitigation: Inspect or back up the target skill directory before installation and avoid installing over local modifications. <br>
Risk: Incorrect input or output paths can process unintended media or overwrite an existing output file. <br>
Mitigation: Specify exact input and output paths, review the generated output path, and prefer upscale.sh presets or explicit WxH values over direct ffmpeg commands. <br>


## Reference(s): <br>
- [Xeonupscale ClawHub release](https://clawhub.ai/wray151/xeonupscale) <br>
- [wray151 publisher profile](https://clawhub.ai/user/wray151) <br>
- [BtbN FFmpeg-Builds releases](https://github.com/BtbN/FFmpeg-Builds/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Shell command invocation with generated MP4 video output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes an MP4 file using H.264 video, Lanczos scaling, and copied audio when possible.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
