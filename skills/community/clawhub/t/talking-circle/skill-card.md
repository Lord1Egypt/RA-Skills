## Description:

Create animated talking-circle videos, like Telegram-style round video messages, from avatar frame images and audio, with audio-to-video and text-to-video support via ElevenLabs or SaluteSpeech TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rai220](https://clawhub.ai/user/rai220)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to generate circular avatar videos from prepared character frames and either an existing audio file or text synthesized through a supported TTS provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The SaluteSpeech text-to-video mode disables TLS verification while sending credentials and user text.

Mitigation: Avoid SaluteSpeech mode until TLS verification is fixed; use existing audio files or another TTS path, and rotate SaluteSpeech credentials that were used on untrusted networks.

Risk: Text-to-video modes send user-provided text to cloud TTS providers.

Mitigation: Use audio-to-video mode with a local or already approved TTS source when text or voice content is sensitive.

Risk: Runtime dependencies are not pinned in the artifact requirements.

Mitigation: Run in a private verified environment with reviewed or pinned dependency versions before production use.

## Reference(s):

- [Talking Circle on ClawHub](https://clawhub.ai/rai220/skills/talking-circle)
- [Frame Preparation Guide](examples/frames/README.md)
- [ElevenLabs](https://elevenlabs.io)
- [ElevenLabs Voice Library](https://elevenlabs.io/voice-library)
- [SaluteSpeech](https://developers.sber.ru/portal/products/smartspeech)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with bash command snippets; scripts generate MP4 video files and build logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.9+, ffmpeg, four matched square PNG frame images, and optional TTS provider credentials for text-to-video modes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
