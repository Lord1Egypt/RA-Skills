## Description: <br>
Voice Notes Pro transcribes WhatsApp voice notes with OpenAI Whisper and categorizes the resulting notes into local Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toniaczlog](https://clawhub.ai/user/toniaczlog) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Users with WhatsApp voice notes use this skill to transcribe audio and organize the text into task, shopping, idea, people, watchlist, and song-note Markdown files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice notes are sent to OpenAI for transcription and may contain personal or sensitive information. <br>
Mitigation: Install only with user consent for this data flow, protect the OpenAI API key, and avoid processing sensitive third-party personal details without permission. <br>
Risk: Transcripts are saved to local Markdown files and may be exposed if the note directory is shared, world-readable, or misconfigured. <br>
Mitigation: Use a user-owned notes directory, restrict filesystem permissions, and review retention expectations before deployment. <br>
Risk: Transcription text is printed to console logs, which can retain private note content. <br>
Mitigation: Review console log retention and disable or restrict transcript logging in environments where notes may be sensitive. <br>


## Reference(s): <br>
- [Voice Notes Pro ClawHub page](https://clawhub.ai/toniaczlog/voice-notes-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [Text responses and Markdown note files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenAI API key, WhatsApp audio input, and writable local note directories.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
