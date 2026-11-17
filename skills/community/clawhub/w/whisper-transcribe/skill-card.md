## Description:

Transcribe audio files to text using OpenAI Whisper with auto language detection, multiple transcript formats, batch processing, and model selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josunlp](https://clawhub.ai/user/josunlp)

### License/Terms of Use:


## Use Case:

Developers, creators, and teams use this skill to transcribe recordings, meetings, lectures, podcasts, voice messages, and supported audio or video files into text or subtitle formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Whisper dependency is installed from the Python package ecosystem and may be unpinned by default.

Mitigation: Install in a virtual environment and pin openai-whisper plus dependencies when stricter supply-chain control is required.

Risk: Transcription creates local output files near the source audio or in the chosen output directory, which may contain sensitive transcript content.

Mitigation: Choose an explicit output directory for sensitive work and review local file handling and retention before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; the wrapped CLI can produce txt, srt, vtt, json, or all transcript files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports tiny, base, small, medium, and large Whisper models; optional language selection, output directory selection, batch inputs, and word-level timestamps.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
