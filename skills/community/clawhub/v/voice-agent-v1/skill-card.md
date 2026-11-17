## Description:

Gives an agent a voice layer that uses ElevenLabs to clone a principal's voice, generate MP3 audio from text, and deploy a conversational AI agent for automated inbound and outbound calls through Twilio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georges91560](https://clawhub.ai/user/georges91560)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, sales teams, and operators use this skill to configure ElevenLabs voice cloning, generate MP3 speech from scripts, and operate Twilio-backed inbound or outbound voice calls. It is intended for voice-enabled outreach and audio content workflows where voice cloning and calling have explicit consent and comply with applicable laws.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives the agent broad account, credential, voice-cloning, and calling authority with weak scoping and plaintext persistence.

Mitigation: Use dedicated ElevenLabs and Twilio accounts, scoped tokens, and a dedicated browser profile; avoid storing account passwords or broad authorization tokens in .env.

Risk: Voice cloning and automated calls can create consent, impersonation, call-recording, telemarketing, and outreach-law risk.

Mitigation: Require explicit consent for voice cloning and confirm compliance with call-recording, telemarketing, and outreach laws before enabling calls.

Risk: Call transcripts, outcomes, and voice-generation status may be sent through Telegram notifications.

Mitigation: Review notification recipients and transcript-sharing practices before use, especially when calls may contain personal or commercial lead information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/georges91560/skills/voice-agent-v1)
- [Publisher Profile](https://clawhub.ai/user/georges91560)
- [ElevenLabs](https://elevenlabs.io)
- [ElevenLabs API](https://api.elevenlabs.io)
- [Twilio API](https://api.twilio.com)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)
- [Artifact Agent Prompt](artifact/agent_prompt.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Audio files, Call logs]

**Output Format:** [Markdown guidance with shell commands, Python code, JSON configuration, generated MP3 audio, and JSON call records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ElevenLabs account/API access for voice cloning and TTS; Twilio credentials are optional for calling; generated credentials and voice/call state are persisted in workspace configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
