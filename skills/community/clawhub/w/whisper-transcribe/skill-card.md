## Description: <br>
Transcribe audio files to text using OpenAI Whisper with auto language detection, multiple output formats, batch processing, and model selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JosunLP](https://clawhub.ai/user/JosunLP) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and operators use this skill to transcribe audio or video recordings such as meetings, lectures, podcasts, voice messages, and interviews into text, subtitle, or JSON outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local transcription depends on Whisper, ffmpeg, and downloaded model files. <br>
Mitigation: Install Whisper, ffmpeg, and model dependencies from trusted sources before use. <br>
Risk: Transcripts and subtitle files are written to the selected output directory. <br>
Mitigation: Review output paths before running the script, especially when processing sensitive audio. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JosunLP/whisper-transcribe) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The transcribe script can generate txt, srt, vtt, json, or all supported transcript formats for local input files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
