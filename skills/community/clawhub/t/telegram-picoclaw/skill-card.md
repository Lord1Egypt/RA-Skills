## Description: <br>
Processes voice conversations in Picoclaw's native Telegram channel by transcribing incoming audio, preparing a text reply, and generating a spoken response without using webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[titara](https://clawhub.ai/user/titara) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Picoclaw operators use this skill to add a local voice-to-voice workflow for Telegram messages: watch for incoming audio, transcribe it, create or finalize a reply, synthesize reply audio, and prepare files for sending back in the same Telegram channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically process private Telegram voice messages and retain transcript metadata locally. <br>
Mitigation: Enable it only for chats and users that have consented to voice processing, restrict the watched folder or chat scope, and define how transcript JSON files and logs are deleted or protected. <br>
Risk: Audio and text may be sent to external speech services for transcription and text-to-speech generation. <br>
Mitigation: Review Groq and Edge TTS data handling requirements before use, configure credentials deliberately, and avoid processing sensitive audio unless that external processing is acceptable. <br>
Risk: A background watcher can continue processing files until stopped. <br>
Mitigation: Document a clear stop procedure, monitor the watcher process, and keep the existing cleanup policy active for generated audio, metadata, and temporary files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/titara/telegram-picoclaw) <br>
- [Implementation plan](references/implementation-plan.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python script commands and generated audio/transcript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GROQ_API_KEY for transcription; produces local transcript metadata JSON and MP3 audio outputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
