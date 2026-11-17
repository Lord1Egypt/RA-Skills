## Description:

Convert audio to SRT subtitles using OpenAI Whisper with automatic GPU acceleration for Intel XPU, NVIDIA CUDA, AMD ROCm, and Apple Metal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allanmeng](https://clawhub.ai/user/allanmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and teams use this skill to generate local SRT subtitle files from audio for videos, meetings, podcasts, courses, and stream recordings. It is intended for agent-assisted transcription workflows that can run Whisper and hardware-matched PyTorch locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First use may download Whisper model files and install unpinned machine-learning dependencies.

Mitigation: Install only where first-run network downloads and pip-installed ML dependencies are acceptable; pre-cache or verify Whisper models for offline or controlled environments.

Risk: Generated subtitles are written beside the source media and may replace a same-name SRT file.

Mitigation: Check for an existing .srt file or choose a separate output directory before processing important media.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/allanmeng/skills/whisper-gpu-transcriber-skill)
- [Project Homepage](https://github.com/allanmeng/whisper-gpu-transcriber-skill)
- [PyTorch CUDA Wheel Index](https://download.pytorch.org/whl/cu121)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated SRT subtitle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces same-directory .srt subtitle files for the selected audio file unless an output directory is supplied.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
