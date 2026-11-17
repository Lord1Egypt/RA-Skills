## Description:

MiniMax TTS Plus generates text-to-speech audio with per-agent voice selection and supports local MP3 generation, Telegram voice messages, and Feishu OGG/Opus voice messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vshen009](https://clawhub.ai/user/vshen009)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to convert agent text into MiniMax-generated speech, choose agent-specific voices, and optionally deliver generated audio through Telegram or Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text and generated audio may be sent to MiniMax and, in delivery modes, to Telegram or Feishu.

Mitigation: Avoid sensitive content unless those services are approved for the data, and use --generate-only when local audio generation is sufficient.

Risk: MiniMax and Telegram credentials are required for some modes and could be exposed if stored carelessly.

Mitigation: Keep MINIMAX_API_KEY and Telegram tokens out of shared folders and repositories, store them in a local .env file, and add .env to the user's own .gitignore.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vshen009/skills/voice-for-openclaw)
- [Publisher profile](https://clawhub.ai/user/vshen009)
- [MiniMax Speech T2A HTTP API](https://platform.minimax.io/docs/api-reference/speech-t2a-http)
- [MiniMax platform](https://platform.minimax.io)
- [Telegram BotFather](https://t.me/BotFather)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [MP3 audio files, OGG/Opus audio files, JSON status strings, and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY; Telegram delivery uses optional Telegram credentials; Feishu voice output requires ffmpeg.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
