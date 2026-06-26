## Description: <br>
Transcribes QQ Bot voice messages by decoding QQ Silk V3 audio and using Whisper speech recognition with Gateway integration and a user confirmation flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cindypapa](https://clawhub.ai/user/cindypapa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QQ Bot operators use this skill to convert incoming QQ voice attachments into text, attach the transcription to bot messages, and request user confirmation before acting on the recognized content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gateway integration examples can pass user-controlled attachment filenames into shell command strings. <br>
Mitigation: Use spawn or execFile with argument arrays, generate safe server-side filenames, and restrict processing to a controlled directory. <br>
Risk: The skill depends on an external Silk decoder path and optional persistent swap configuration. <br>
Mitigation: Pin the decoder to a trusted location and enable swap instructions only after intentionally approving the system-level change. <br>
Risk: Voice messages may contain sensitive content that is transcribed, logged, or stored. <br>
Mitigation: Disclose transcription behavior to bot users and apply retention, access control, and logging policies before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cindypapa/qqbot-voice-transcribe) <br>
- [silk-v3-decoder](https://github.com/kn007/silk-v3-decoder) <br>
- [Whisper](https://github.com/openai/whisper) <br>
- [OpenClaw QQ Bot](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command snippets, Python and TypeScript examples, and generated transcription text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg, python3, git, whisper, and a trusted Silk V3 decoder path; Gateway examples should be adapted before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and changelog state 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
