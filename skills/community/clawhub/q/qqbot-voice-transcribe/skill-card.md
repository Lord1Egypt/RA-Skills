## Description:

Transcribes QQ Bot voice messages by decoding QQ Silk V3 audio and running Whisper, with examples for Gateway integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindypapa](https://clawhub.ai/user/cindypapa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bot operators use this skill to add transcription of QQ .amr and .silk voice attachments to QQ Bot workflows. The skill provides scripts and integration examples that convert voice messages into text for display or review in the bot flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gateway examples expose bot hosts to command injection through shell execution.

Mitigation: Replace shell exec examples with execFile or spawn argument arrays, generate safe server-side filenames, and sanitize all paths before deployment.

Risk: The release claims confirmation and safety controls that are not actually implemented.

Mitigation: Add a real opt-in confirmation step before any downstream bot action uses a voice transcript.

Risk: Voice transcripts can contain sensitive user content.

Mitigation: Define privacy handling and log-retention limits for audio files, transcripts, paths, and recognition logs.

Risk: Swap and fstab instructions can alter host-level system configuration.

Mitigation: Run under a dedicated low-privilege account and apply swap or fstab changes only with explicit administrator approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cindypapa/skills/qqbot-voice-transcribe)
- [silk-v3-decoder](https://github.com/kn007/silk-v3-decoder)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and Python or TypeScript code examples; transcription scripts produce plain text and optional JSON batch reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local audio files and external binaries including ffmpeg, Python 3, Whisper, git, and silk-v3-decoder.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog state 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
