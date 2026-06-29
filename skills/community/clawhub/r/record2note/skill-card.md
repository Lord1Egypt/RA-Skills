## Description: <br>
Use when converting voice recordings, voice memos, or speech transcripts into structured Markdown notes, setting up recording-folder monitoring, or processing pending transcription files on macOS or Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soullhcn](https://clawhub.ai/user/soullhcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and note-taking workflows use Record2Note to turn local audio recordings or existing transcripts into structured Markdown notes with summaries, key points, action items, timestamps, and optional speaker labels. It supports manual processing and background folder monitoring on macOS or Windows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create background monitoring services that watch local recording folders. <br>
Mitigation: Enable automatic monitoring only after reviewing the configuration; start with manual processing until the watch and archive paths are confirmed. <br>
Risk: The setup can install or build dependencies and download large speech models. <br>
Mitigation: Review dependency and package-manager changes before setup, choose the smallest model that meets quality needs, and confirm disk and network constraints before downloads. <br>
Risk: Transcript content may be passed to a detected external agent CLI. <br>
Mitigation: Set agent_cli to none for local-only transcription or when transcripts contain sensitive content; explicitly choose a trusted CLI only after review. <br>
Risk: Processing workflows can write notes, move archived audio, and delete processed watch files or pending JSON. <br>
Mitigation: Keep backups of original audio, verify archive paths, and test with non-critical recordings before enabling deletion or archive automation. <br>
Risk: Optional speaker diarization requires additional dependencies and may involve Hugging Face model access. <br>
Mitigation: Disable diarization unless speaker labels are needed and review account, model terms, and dependency requirements before enabling it. <br>


## Reference(s): <br>
- [Record2Note ClawHub release page](https://clawhub.ai/soullhcn/skills/record2note) <br>
- [whisper.cpp releases](https://github.com/ggerganov/whisper.cpp/releases) <br>
- [pyannote speaker diarization 3.1](https://huggingface.co/pyannote/speaker-diarization-3.1) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown notes, JSON pending records, and shell or PowerShell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated notes may include frontmatter, summaries, key points, action items, timestamps, transcript text, and optional Obsidian formatting.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
