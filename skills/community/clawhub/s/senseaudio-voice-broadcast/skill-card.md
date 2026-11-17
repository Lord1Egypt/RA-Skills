## Description:

Turns plain text into persona-driven TTS scripts for narration, companion-style voice messages, emotional comfort audio, and expressive spoken responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jsinbupt](https://clawhub.ai/user/jsinbupt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use SenseAudio to convert written text into natural, persona-driven spoken scripts with tone, pacing, and style guidance. When audio output is requested, the skill can provide or run a SenseAudio TTS command that saves generated audio locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio generation can send text and API credentials over the network with weak endpoint and download controls.

Mitigation: Use script-only output for sensitive content, and generate audio only when the text is appropriate to send to SenseAudio.

Risk: Using a custom or untrusted TTS endpoint can expose credentials or return unsafe media URLs.

Mitigation: Do not pass a custom --url or untrusted endpoint unless the script is changed to bind credentials to approved hosts, validate returned media URLs, and enforce timeouts and size limits.

## Reference(s):

- [SenseAudio TTS API Notes](references/senseaudio-api.md)
- [Voice Broadcast Templates](references/voice-broadcast-templates.md)
- [SenseAudio TTS Wrapper](scripts/senseaudio_tts.py)
- [ClawHub Skill Page](https://clawhub.ai/jsinbupt/skills/senseaudio-voice-broadcast)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown with spoken-script sections, TTS style notes, optional bash commands, and optional local audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese unless another language is requested; audio generation requires a SenseAudio API key.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
