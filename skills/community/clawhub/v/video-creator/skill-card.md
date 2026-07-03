## Description: <br>
Video Creator helps an agent assemble product introduction videos from scripts and images, with text-to-speech narration, optional cloned voice, synchronized subtitles, and optional portrait narration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coolalam](https://clawhub.ai/user/coolalam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect video requirements, prepare script and media inputs, and run a video-generation workflow for product demos, promotional clips, narrated slideshows, and short portrait narration segments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload scripts, generated prompts, portrait photos, audio, and voice samples to platform.delilegal.com or OSS-backed services for cloud processing. <br>
Mitigation: Use only non-sensitive, consented media and review the configured API key and destination service before enabling cloud-backed voice, image, or portrait-video features. <br>
Risk: The skill can persist API keys or voice identifiers in voice_config.json. <br>
Mitigation: Store only scoped credentials, inspect voice_config.json before sharing the skill directory, and rotate credentials if the file is exposed. <br>
Risk: The main generation script clears the selected output directory before writing new results. <br>
Mitigation: Point --output to a dedicated disposable directory and avoid using any directory that contains source images or other user data. <br>
Risk: The skill depends on local Python packages and ffmpeg, and setup may modify the Python environment. <br>
Mitigation: Install dependencies in a controlled virtual environment or disposable workspace before running the scripts. <br>


## Reference(s): <br>
- [Dependencies](references/dependencies.md) <br>
- [Alibaba Cloud Model Studio Text-to-Speech Documentation](https://help.aliyun.com/zh/model-studio/text-to-speech) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with command examples and generated MP4, SRT, audio, and image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce video files, subtitle files, segment audio, generated images, and updated voice configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
