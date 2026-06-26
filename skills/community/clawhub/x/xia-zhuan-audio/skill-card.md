## Description: <br>
音视频格式转换与处理工具箱，基于 FFmpeg and Whisper AI，支持格式转换、视频提取音频、合并、分割、压缩、查看信息、音频转文字。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luis1213899](https://clawhub.ai/user/luis1213899) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to convert, extract, merge, split, compress, inspect, and transcribe local audio or video files through OpenClaw prompts or command-line tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local FFmpeg and Python tools operate on files selected by the user and may overwrite generated output paths. <br>
Mitigation: Use explicit output paths, review destination filenames before execution, and keep originals backed up. <br>
Risk: First transcription use can download and cache a Whisper model from Hugging Face or a configured mirror. <br>
Mitigation: Use a trusted HF_ENDPOINT and XZA_MODELDIR, and allow model downloads only in environments where that network access and storage are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luis1213899/xia-zhuan-audio) <br>
- [Project homepage](https://github.com/luis12123899/xia-zhuan-audio) <br>
- [FFmpeg](https://ffmpeg.org) <br>
- [Hugging Face](https://huggingface.co) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Console text plus generated audio, subtitle, transcript, or JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local output paths and formats are selected by the user; transcription can emit txt, srt, vtt, or json.] <br>

## Skill Version(s): <br>
1.3.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
