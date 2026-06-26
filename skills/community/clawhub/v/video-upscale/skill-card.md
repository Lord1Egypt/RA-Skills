## Description: <br>
AI-powered video upscaling with Real-ESRGAN and Waifu2x. Use when user asks to enhance, upscale, improve video quality, make HD/4K. Supports anime and real footage with progress tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NightVibes3](https://clawhub.ai/user/NightVibes3) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to upscale short video files to HD or 4K-style outputs, choosing anime or real-footage modes and fast or high-quality presets. It is intended for local video enhancement workflows that can install and run ffmpeg, Real-ESRGAN, and Waifu2x tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted inputs to the shell wrapper could trigger unintended local command execution. <br>
Mitigation: Use Review-level caution, sanitize JOB_ID and other caller-controlled values before use, quote cleanup handling safely, and run only after constraining or patching the script. <br>
Risk: The skill relies on externally installed upscaling binaries. <br>
Mitigation: Install binaries only from trusted sources and verify downloaded upscaling artifacts before use. <br>


## Reference(s): <br>
- [Installation Guide](references/INSTALL.md) <br>
- [Real-ESRGAN NCNN Vulkan Release](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-ubuntu.zip) <br>
- [Waifu2x NCNN Vulkan Release](https://github.com/nihui/waifu2x-ncnn-vulkan/releases/download/20220728/waifu2x-ncnn-vulkan-20220728-ubuntu.zip) <br>
- [ClawHub Skill Page](https://clawhub.ai/NightVibes3/video-upscale) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and line-oriented job status output from the video upscaling script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script reports phases, frame counts, progress, final status, and the output video path.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
