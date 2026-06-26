## Description: <br>
Convert audio to SRT subtitles using OpenAI Whisper with automatic GPU acceleration for Intel XPU, NVIDIA CUDA, AMD ROCm, and Apple Metal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allanmeng](https://clawhub.ai/user/allanmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, meeting organizers, podcast producers, course authors, and developers use this skill to transcribe local audio files into SRT subtitle files with hardware acceleration when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python transcription code and requires Whisper and PyTorch dependencies. <br>
Mitigation: Install and run it only in an environment where local Python execution and those dependencies are approved. <br>
Risk: The first transcription may download a large Whisper model and cache it locally. <br>
Mitigation: Confirm storage, network, and model-cache location before first use. <br>
Risk: The transcription script writes .srt files next to selected audio files or in a requested output directory, which may overwrite an existing subtitle file with the same base name. <br>
Mitigation: Review the chosen audio path and output directory, and keep backups of existing subtitle files before running. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allanmeng/whisper-gpu-transcriber-skill) <br>
- [Project homepage](https://github.com/allanmeng/whisper-gpu-transcriber-skill) <br>
- [PyTorch CUDA wheel index](https://download.pytorch.org/whl/cu121) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [SRT subtitle file with optional Markdown guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or overwrites a .srt file next to the selected audio file or in the requested output directory.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
