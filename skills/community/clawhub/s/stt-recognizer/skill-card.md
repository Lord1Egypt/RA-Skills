## Description: <br>
Records microphone audio and transcribes speech to text with local Whisper/faster-whisper models or an OpenAI-compatible API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moroiser](https://clawhub.ai/user/moroiser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to capture short microphone recordings, transcribe existing audio files, and save transcripts using local or API-backed speech-to-text engines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture microphone audio and save speech recordings or transcripts to disk. <br>
Mitigation: Use it only with clear user intent and consent, verify the output directory before recording, and delete recordings or transcripts that are no longer needed. <br>
Risk: API mode can send audio to a remote OpenAI-compatible transcription service. <br>
Mitigation: Prefer local-only transcription for sensitive speech and configure API URL and credentials deliberately when remote processing is acceptable. <br>
Risk: Broad automatic triggers in shared or private environments could lead to unintended audio capture. <br>
Mitigation: Keep invocation explicit and avoid enabling always-on or automatic use in environments where private conversation may be present. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moroiser/stt-recognizer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; runtime output is plain text transcripts and WAV recordings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May access microphone input, write recordings and transcripts under the OpenClaw workspace, and send audio to a configured remote API in API mode.] <br>

## Skill Version(s): <br>
1.0.8 (source: server evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
