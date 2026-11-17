## Description:

Use when converting voice recordings, voice memos, or speech transcripts into structured Markdown notes, setting up recording-folder monitoring, or processing pending transcription files on macOS or Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soullhcn](https://clawhub.ai/user/soullhcn)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and note-taking workflows use Record2Note to transcribe recordings or voice memos, generate structured Markdown notes, and optionally maintain recording-folder monitoring on macOS or Windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Background monitoring can process new files automatically.

Mitigation: Avoid enabling automatic monitoring until watch directories, archive paths, and sync behavior are configured and reviewed.

Risk: Automatic agent triggering can send transcripts and file paths to another AI CLI.

Mitigation: Set agent_cli to none unless the user explicitly wants downstream agent processing.

Risk: Processed recordings may be archived and originals removed from the watch folder.

Mitigation: Preserve originals or keep a separate backup before processing recordings.

Risk: Dependency setup can download binaries, models, or build code.

Mitigation: Review before installation and prefer official dependency sources with pinned hashes.

Risk: Configuration values affect shell execution on macOS.

Mitigation: Inspect config.json before running setup, processing, or background monitoring.

## Reference(s):

- [Record2Note ClawHub Release](https://clawhub.ai/soullhcn/skills/record2note)
- [whisper.cpp releases](https://github.com/ggerganov/whisper.cpp/releases)
- [pyannote speaker diarization 3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)
- [Syncthing downloads](https://syncthing.net/downloads/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, JSON pending transcription records, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save notes to the configured vault, save pending transcript JSON, archive processed audio, and remove watch-folder originals after successful processing.]

## Skill Version(s):

1.1.0 (source: server release metadata, created 2026-06-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
