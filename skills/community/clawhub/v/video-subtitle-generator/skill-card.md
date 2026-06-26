## Description: <br>
Generate and translate video subtitles using WhisperX and LLM translation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jianhua-Cui](https://clawhub.ai/user/Jianhua-Cui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and video localization workflows use this skill to transcribe video files into timestamped SRT subtitles and optionally translate them into target-language or bilingual subtitle files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Translation may send subtitle text to the configured LLM provider. <br>
Mitigation: Avoid translating sensitive videos unless the user accepts the provider, endpoint, and data-sharing implications. <br>
Risk: Translation may incur token-based API costs. <br>
Mitigation: Confirm the API key, base URL, model, target language, and cost acknowledgement before running translation or the full pipeline. <br>
Risk: Dependency installation and Whisper model downloads can consume significant disk space and bandwidth. <br>
Mitigation: Use a virtual environment, consider pinning dependencies, and confirm storage and download expectations before installing packages or downloading models. <br>


## Reference(s): <br>
- [WhisperX](https://github.com/m-bain/whisperX) <br>
- [FFmpeg](https://ffmpeg.org/) <br>
- [OpenRouter API endpoint](https://openrouter.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash commands; execution produces SRT subtitle files and JSON transcription metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcription runs locally after model download; translation can call a configured LLM API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
