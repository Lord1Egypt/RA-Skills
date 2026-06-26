## Description: <br>
Turbo Whisper Local STT helps an agent transcribe local audio files or folders with Faster-Whisper, optimized for Chinese speech, VAD chunking, and text or JSON transcript output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangminrui2022](https://clawhub.ai/user/wangminrui2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn recordings, meetings, interviews, voice notes, and extracted audio for subtitles into local transcript files. It is intended for audio files or folders and can produce batch transcripts while preserving directory structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install or alter Python packages and download large transcription models. <br>
Mitigation: Review before installing, run in a controlled environment, and prefer preinstalled dependencies and a local model path when network downloads are not acceptable. <br>
Risk: Transcripts and logs may contain sensitive speech content. <br>
Mitigation: Choose protected output directories, limit access to generated transcript and log files, and delete artifacts according to local data-handling requirements. <br>
Risk: Offline privacy claims depend on model availability; first use may still require downloading models. <br>
Mitigation: Use a preinstalled local model path for true offline operation and verify the environment does not need network access before processing sensitive audio. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangminrui2022/turbo-whisper-local-stt) <br>
- [faster-whisper base CT2 model](https://huggingface.co/wangminrui2022/faster-whisper-base-ct2) <br>
- [faster-whisper large-v3 CT2 model](https://huggingface.co/wangminrui2022/faster-whisper-large-v3-ct2) <br>
- [faster-whisper large-v3 turbo CT2 model](https://huggingface.co/deepdml/faster-whisper-large-v3-turbo-ct2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands] <br>
**Output Format:** [Plain text and JSON transcript files with command-oriented agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include full transcript text, segments, timestamps, and generated file paths; default behavior may create both text and JSON outputs.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
