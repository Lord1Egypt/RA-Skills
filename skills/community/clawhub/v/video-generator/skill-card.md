## Description: <br>
Automated text-to-video pipeline with multi-provider TTS/ASR support - OpenAI, Azure, Aliyun, Tencent | 多厂商 TTS/ASR 支持的自动化文本转视频系统 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhenstaff](https://clawhub.ai/user/zhenstaff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn text scripts into short vertical videos with voiceover, timestamping, scene orchestration, and local rendering. It supports provider configuration for OpenAI, Azure, Aliyun, or Tencent TTS/ASR services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger package installs, repository clones, video generation, and cloud API calls that may create cost, supply-chain, or execution risk. <br>
Mitigation: Verify the intended package or source before use and require explicit confirmation before clone, install, generation, or provider API calls. <br>
Risk: Provider credentials and user scripts may be exposed through commands, logs, or submitted to cloud TTS/ASR providers. <br>
Mitigation: Use limited-scope API keys, avoid printing .env contents, monitor provider billing, and do not submit confidential scripts unless the provider is approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhenstaff/video-generator) <br>
- [Project homepage](https://github.com/ZhenRobotics/openclaw-video-generator#readme) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash code blocks and generated local media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local MP4 video files, audio files, timestamp JSON, and scene configuration when the referenced generator is installed and configured.] <br>

## Skill Version(s): <br>
1.0.42 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
