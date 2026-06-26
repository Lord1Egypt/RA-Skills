## Description: <br>
Generic Xeon-CPU video upscaler that plans Lanczos pre-scaling plus Real-ESRGAN general-x4v3 passes to reach a target resolution with super-resolution as the final step. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wray151](https://clawhub.ai/user/wray151) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video-processing users use this skill to install and run a CPU-based video upscaling pipeline for MP4 inputs at common preset resolutions or explicit WxH targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer bootstraps pip, installs Python packages, or downloads static ffmpeg content from the internet without checksum or signature verification. <br>
Mitigation: Review the installer before use, avoid sudo, prefer trusted system package managers for pip and ffmpeg, and install in a disposable environment. <br>
Risk: Video processing runs local scripts and bundled model assets over user-provided media files. <br>
Mitigation: Run on trusted input files in a constrained workspace and review generated output before relying on it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wray151/xeon-smartupscale-v2) <br>
- [PyPA get-pip bootstrap](https://bootstrap.pypa.io/get-pip.py) <br>
- [Static ffmpeg download archive](https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides installation and execution of scripts that produce H.264 MP4 video output.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
