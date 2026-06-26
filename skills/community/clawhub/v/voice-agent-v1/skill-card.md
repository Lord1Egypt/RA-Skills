## Description: <br>
Gives an agent a voice layer that can clone a principal's voice with ElevenLabs, generate MP3 speech from text, and support inbound or outbound conversational calls through Twilio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add voice cloning, text-to-speech audio generation, and lead call handling to an agent workflow. It is intended for workflows that need MP3 content, prospect qualification calls, call transcripts, and Telegram status notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad access to ElevenLabs, possible browser login sessions or account credentials, voice samples, Twilio calling credentials, lead phone data, and call transcripts. <br>
Mitigation: Use scoped API keys stored in a secret manager, require explicit approval before login, key creation, voice cloning, Twilio connection, or outbound calls, and rotate credentials on a defined schedule. <br>
Risk: Voice cloning and automated calls can create consent, disclosure, and impersonation concerns if used without clear controls. <br>
Mitigation: Define consent, caller disclosure, opt-out, shutdown, and approved-use procedures before deployment, and test with internal numbers before calling external contacts. <br>
Risk: Call transcripts, lead phone data, and generated audio may contain sensitive personal or business information. <br>
Mitigation: Set transcript retention, redaction, access-control, and deletion rules before use, and avoid storing secrets or sensitive data in shared .env files. <br>


## Reference(s): <br>
- [Voice Agent ClawHub page](https://clawhub.ai/georges91560/voice-agent-v1) <br>
- [ElevenLabs](https://elevenlabs.io) <br>
- [ElevenLabs API](https://api.elevenlabs.io) <br>
- [Twilio API](https://api.twilio.com) <br>


## Skill Output: <br>
**Output Type(s):** [Audio files, Configuration, Shell commands, Guidance] <br>
**Output Format:** [MP3 audio, JSON configuration, Markdown guidance, and shell-command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate call logs, transcripts, Telegram notifications, and service configuration for ElevenLabs and Twilio.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
