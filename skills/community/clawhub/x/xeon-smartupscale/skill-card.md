## Description: <br>
Xeon Smartupscale upscales videos on Linux x86_64 by combining ffmpeg Lanczos pre-scaling with ETDS 2x OpenVINO CPU super-resolution for target resolutions such as 1080p, 1440p, and 4K. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wray151](https://clawhub.ai/user/wray151) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video-processing users can use this skill to generate shell commands for installing and running a CPU-based video upscaling workflow. It targets arbitrary output resolutions while preserving aspect ratio for height presets and emits H.264 MP4 output with original audio merged when present. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can download and execute third-party code or binaries without integrity checks. <br>
Mitigation: Review install.sh before use, install in a disposable environment, and prefer system-provided ffmpeg and an already configured pip installation. <br>
Risk: Generated outputs may overwrite existing video files when an output path is reused. <br>
Mitigation: Use a new explicit output filename for each run and verify the destination path before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wray151/xeon-smartupscale) <br>
- [Publisher profile](https://clawhub.ai/user/wray151) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides use of a local video-processing pipeline that writes MP4 output files.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
