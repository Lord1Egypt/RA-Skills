## Description:

Transcribes local audio files and folders with Faster-Whisper, optimized for Chinese speech, long-audio VAD segmentation, GPU acceleration, and text or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangminrui2022](https://clawhub.ai/user/wangminrui2022)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to transcribe meeting recordings, interviews, voice notes, and audio folders into local text or JSON outputs. It can also create segmented audio/text assets and metadata files for downstream speech workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports broad automatic pip installs and Hugging Face downloads despite local/offline positioning.

Mitigation: Install and run only in a sandbox or dedicated virtual environment, and prefer a reviewed local --model_path for offline execution.

Risk: Model repository names can be supplied at runtime, which can cause unreviewed remote model downloads.

Mitigation: Use only trusted, pinned model repositories or pre-downloaded local model directories.

Risk: The skill can write logs, transcripts, model cache data, segmented audio, and metadata files.

Mitigation: Run it only where those files are acceptable, and direct outputs to a controlled directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangminrui2022/skills/turbo-whisper-local-stt)
- [faster-whisper-base-ct2 model](https://huggingface.co/wangminrui2022/faster-whisper-base-ct2)
- [faster-whisper-large-v3-ct2 model](https://huggingface.co/wangminrui2022/faster-whisper-large-v3-ct2)
- [faster-whisper-large-v3-turbo-ct2 model](https://huggingface.co/deepdml/faster-whisper-large-v3-turbo-ct2)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with bash command examples, plus generated .txt, .json, .wav, and metadata.list files at runtime]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch mode preserves input directory structure; runtime may create a virtual environment, model cache, logs, transcript files, segmented audio, and metadata outputs.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
