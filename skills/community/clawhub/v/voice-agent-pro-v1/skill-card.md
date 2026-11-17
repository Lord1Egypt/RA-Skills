## Description:

Gives an OpenClaw agent a voice layer that uses ElevenLabs for voice cloning and text-to-speech, with optional Twilio calling and Telegram notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georges91560](https://clawhub.ai/user/georges91560)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure voice cloning, generate MP3 narration from text, and support lead follow-up or qualification workflows through optional phone calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles voice cloning and may upload voice samples to ElevenLabs.

Mitigation: Use only with explicit consent from the voice owner and confirm that users understand where samples are sent before setup.

Risk: The skill requests persistent API credentials and may store sensitive keys in plaintext configuration.

Mitigation: Prefer scoped secrets or a protected secret store, and avoid storing production credentials in plaintext config.json.

Risk: Telegram and Twilio credentials can enable notifications and phone call workflows beyond basic text-to-speech.

Mitigation: Grant Telegram or Twilio credentials only when those workflows are intentionally enabled, and review call behavior before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/georges91560/skills/voice-agent-pro-v1)
- [Publisher Profile](https://clawhub.ai/user/georges91560)
- [Setup Guide](artifact/setup_guide.md)
- [ElevenLabs API](https://api.elevenlabs.io)
- [Twilio API](https://api.twilio.com)
- [Telegram Bot API](https://api.telegram.org)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, MP3 audio files, JSON call records]

**Output Format:** [Markdown instructions, Python CLI commands, JSON configuration, and generated MP3 files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided API credentials and voice samples; optional call workflows require Twilio credentials.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
