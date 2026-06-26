## Description: <br>
Local speech-to-text using OpenAI Whisper for transcribing audio files, voice messages, and recordings across many languages with local processing and session-isolated outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lkisme](https://clawhub.ai/user/lkisme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and run a local Whisper-based speech-to-text workflow for audio files, voice messages, meeting recordings, batch transcription, and multi-agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation may change system packages and download Whisper dependencies and model files. <br>
Mitigation: Review the setup script before running it, install in a controlled environment, and confirm system package changes are acceptable. <br>
Risk: Transcript files may not be safely constrained to the documented output folder. <br>
Mitigation: Use simple session IDs containing only letters, numbers, dashes, or underscores, and inspect output paths until path validation is fixed. <br>
Risk: Generated transcripts can contain sensitive local audio content. <br>
Mitigation: Treat transcript outputs as sensitive files and apply local retention, access-control, and cleanup practices appropriate for the source audio. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lkisme/sst-simple) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Plain text transcripts, JSON command responses, transcript files, and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local transcript files under the documented stt_output directory; Whisper CLI can also produce subtitle formats.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
