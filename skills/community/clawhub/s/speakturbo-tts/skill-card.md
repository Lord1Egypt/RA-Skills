## Description:

Speak Turbo gives agents ultra-fast local text-to-speech with built-in voices, audio playback, and roughly 90 ms warm-daemon latency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emzod](https://clawhub.ai/user/emzod)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to make an assistant speak responses aloud locally, either playing generated audio immediately or saving WAV output for later use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer fetches unpinned dependencies and builds local code.

Mitigation: Review the package before installing, run it in an isolated environment when possible, and pin or verify dependencies before use.

Risk: The skill runs a localhost text-to-speech daemon without authentication or resource limits.

Mitigation: Use it only on trusted machines, stop the daemon when finished, and avoid exposing the local port beyond the host.

Risk: Sensitive text may be spoken aloud or written to audio files.

Mitigation: Avoid sending secrets or private content to the skill and keep output directories narrowly scoped.

## Reference(s):

- [Speak Turbo ClawHub page](https://clawhub.ai/emzod/skills/speakturbo-tts)
- [Speak Turbo website](https://speakturbo-site.vercel.app)
- [Pocket TTS](https://github.com/kyutai-labs/pocket-tts)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, audio files]

**Output Format:** [Markdown guidance with inline shell commands and optional WAV audio output from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can play audio locally or save 24 kHz mono WAV files; first run may take 2-5 seconds while the daemon loads.]

## Skill Version(s):

1.0.7 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
