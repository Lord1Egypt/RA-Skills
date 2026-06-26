## Description: <br>
Provides Whisper-based ASR and Edge TTS helpers for OpenClaw, including agent-specific voices and an optional Telegram voice reply script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[believe3344](https://clawhub.ai/user/believe3344) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to transcribe incoming audio to text, synthesize replies as MP3 speech, and send Telegram voice replies when explicitly invoked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice content may be processed by local Whisper and cloud Edge TTS. <br>
Mitigation: Review data handling requirements before deployment and avoid sensitive audio or reply text unless this processing path is approved. <br>
Risk: Telegram bot tokens are read from OpenClaw config, command-line input, or environment variables, and messages are sent to supplied chat IDs. <br>
Mitigation: Use scoped bot tokens, verify chat IDs before sending, restrict token access, rotate credentials when needed, and prefer explicit channel allowlists. <br>
Risk: Local OpenClaw configuration is evaluated as code. <br>
Mitigation: Use strict JSON config parsing and review local configuration files before installing or enabling the skill. <br>
Risk: Successful ASR can copy inbound audio into the workspace and delete the original inbound file. <br>
Mitigation: Use opt-in non-destructive archiving or a retention policy that preserves required originals before deletion. <br>
Risk: Transcripts are emitted in agent-facing text that may steer later agent behavior. <br>
Mitigation: Treat transcript text as untrusted user content and require user or application validation before following transcript-embedded instructions. <br>


## Reference(s): <br>
- [Voice TTS/ASR ClawHub Page](https://clawhub.ai/believe3344/voice-tts) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration] <br>
**Output Format:** [Plain text transcripts, MP3 audio files, JSON status objects, and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or newer, Python 3, ffmpeg, edge-tts, whisper, and click; Telegram sending requires a bot token and target chat ID.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
