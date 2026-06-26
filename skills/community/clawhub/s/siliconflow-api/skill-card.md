## Description: <br>
SiliconFlow API integrates SiliconFlow media-generation capabilities for text-to-image, image-to-image, text-to-video, image-to-video, and text-to-speech workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mr-j-j](https://clawhub.ai/user/mr-j-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure a SiliconFlow API key and run shell commands that generate images, videos, speech audio, list models, and check asynchronous video jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a SiliconFlow API key locally in .sf-config.json. <br>
Mitigation: Keep the config file private, restrict filesystem access, and remove the file when the key is no longer needed. <br>
Risk: Prompts, speech text, and selected image files are sent to SiliconFlow for generation. <br>
Mitigation: Avoid confidential or regulated content unless SiliconFlow is approved for that data and use case. <br>
Risk: Temporary request files and generated outputs may remain under /tmp. <br>
Mitigation: Clean /tmp request and output files after use, especially when working with sensitive images or text. <br>
Risk: Generation calls consume the user's SiliconFlow account balance. <br>
Mitigation: Review prompts, durations, and model choices before running commands, particularly for video generation. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/mr-j-j/siliconflow-api) <br>
- [SiliconFlow](https://siliconflow.cn) <br>
- [SiliconFlow API models endpoint](https://api.siliconflow.cn/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Text] <br>
**Output Format:** [Bash command invocations with generated image, video, and audio files plus status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SiliconFlow API key; generated outputs and temporary request files may be written under /tmp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
