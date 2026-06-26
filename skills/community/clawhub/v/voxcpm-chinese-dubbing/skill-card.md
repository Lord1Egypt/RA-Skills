## Description: <br>
Video Dubbing helps agents convert foreign-language videos into Chinese dubbed videos using Whisper transcription, API-based translation, VoxCPM TTS, subtitle generation, and optional background music. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newaiguy](https://clawhub.ai/user/newaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content localization teams use this skill to produce Chinese-dubbed versions of foreign-language videos, including translated speech, generated subtitles, and final media files. It is also useful when an agent needs repeatable shell-command guidance for configuring VoxCPM, translation APIs, and media processing tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcript text and at least one extracted video frame may be sent to configured model APIs. <br>
Mitigation: Use trusted endpoints, scoped API keys, and review the input media for sensitive content before running the dubbing workflow. <br>
Risk: The bundled Bilibili upload script can use local session credentials to publish videos under the configured account. <br>
Mitigation: Remove or ignore scripts/upload_bilibili.py unless Bilibili publishing is intended, and do not place credentials at the hard-coded path unless that behavior is acceptable. <br>
Risk: Voice cloning depends on user-provided reference audio. <br>
Mitigation: Use only reference voices that the operator has permission to use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/newaiguy/voxcpm-chinese-dubbing) <br>
- [VoxCPM](https://github.com/modelscope/VoxCPM) <br>
- [OpenAI Whisper](https://github.com/openai/whisper) <br>
- [Hunyuan-MT-7B](https://huggingface.co/tencent/Hunyuan-MT-7B) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands, JSON configuration, and generated MP4, WAV, and SRT files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written under the configured workspace and may depend on local ffmpeg, Whisper, VoxCPM, and configured model API endpoints.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
