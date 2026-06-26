## Description: <br>
One-command YouTube video transcription that first uses available captions and falls back to downloading audio for OpenAI Whisper API transcription when captions are unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EdisonChenAI](https://clawhub.ai/user/EdisonChenAI) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and content analysts use this skill in an agent session to create transcripts from YouTube videos, including videos without captions, for review, summarization, or note-taking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio may be uploaded to OpenAI when captions are unavailable or Whisper transcription is forced. <br>
Mitigation: Use only YouTube audio you are allowed to send to OpenAI, avoid sensitive or confidential recordings, and confirm API use before running Whisper transcription. <br>
Risk: Custom output paths were flagged by the security review as unsafe. <br>
Mitigation: Prefer the default /tmp transcript path or carefully review custom output paths until path handling is fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EdisonChenAI/youtube-transcriber) <br>
- [Claude Code](https://claude.com/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain text transcript saved to a file, with the output path printed to stdout.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can use existing subtitles or call OpenAI Whisper API; custom language, output path, Whisper forcing, audio retention, and bitrate options are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
