## Description: <br>
Video Creator helps an agent turn product scripts and image assets into narrated product videos with optional cloned voice, edge-tts narration, synchronized SRT subtitles, and portrait-based talking-head segments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolalam](https://clawhub.ai/user/coolalam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content operators use this skill to assemble product introduction, promotional, demo, and talking-head videos from scripts, images, voice preferences, and subtitle choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice samples, portraits, generated media, and related prompts may be uploaded to platform.delilegal.com or OSS when remote AI features are used. <br>
Mitigation: Use only media the user is authorized to process, avoid sensitive personal media unless the environment permits it, and disclose remote upload behavior before execution. <br>
Risk: API keys and voice identifiers can be stored in plaintext voice_config.json. <br>
Mitigation: Use restricted or disposable keys, keep real secrets out of shared workspaces and commits, and rotate credentials after use when appropriate. <br>
Risk: The scripts can install Python packages at runtime and rely on ffmpeg subprocess execution. <br>
Mitigation: Preinstall dependencies in a controlled virtual environment or container and review the installed packages and system binary paths before running the generation workflow. <br>
Risk: The generation workflow can clear the user-selected output directory before creating video artifacts. <br>
Mitigation: Set --output to a dedicated disposable directory and avoid pointing it at folders containing source assets or unrelated user files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coolalam/skills/video-creator) <br>
- [Dependency installation guide](artifact/references/dependencies.md) <br>
- [Alibaba Cloud Model Studio text-to-speech documentation](https://help.aliyun.com/zh/model-studio/text-to-speech) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with CLI commands; generated artifacts can include MP4 video, SRT subtitles, audio segments, and image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may use local ffmpeg, edge-tts, and Pillow paths, and may call remote platform services when voice cloning, online image generation, or talking-head video generation is requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
