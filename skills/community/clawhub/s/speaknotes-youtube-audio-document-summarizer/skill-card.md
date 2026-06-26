## Description: <br>
Use when OpenClaw needs to call SpeakNotes API routes directly using an API key and generate transcripts/summaries from YouTube URLs, media files, or document files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JackLillie](https://clawhub.ai/user/JackLillie) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to call SpeakNotes APIs for YouTube, media-file, and document summarization workflows, including upload setup, note status polling, note retrieval, and folder retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a SpeakNotes API key to upload selected content and read notes or folders in the connected SpeakNotes account. <br>
Mitigation: Use a dedicated revocable API key stored in OpenClaw secrets or config, and only process files, YouTube URLs, notes, and folders that the user intends to share with SpeakNotes. <br>
Risk: API keys or account data could be exposed if requests are sent to an untrusted host or logged during execution. <br>
Mitigation: Send requests only to https://api.speaknotes.io, avoid printing or logging API keys, and keep the SPEAKNOTES_API_KEY value in the configured secret store. <br>
Risk: Optional device-token fields such as fcmToken can add unnecessary account or notification exposure. <br>
Mitigation: Do not provide fcmToken or similar device-token values unless the user explicitly needs that behavior and understands why it is required. <br>


## Reference(s): <br>
- [SpeakNotes OpenClaw Integration](https://speaknotes.io/integrations/openclaw) <br>
- [SpeakNotes API Host](https://api.speaknotes.io) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, configuration, text] <br>
**Output Format:** [Markdown guidance with structured response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent responses should include action, endpoints_used, noteId when applicable, status, result, and next_step.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
