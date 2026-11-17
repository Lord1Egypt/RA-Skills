## Description:

Converts text replies into speech with Noiz AI TTS, saves generated audio locally, and can play it automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richardx0319](https://clawhub.ai/user/richardx0319)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Voice Reply to turn assistant replies, direct text, or subtitle text into spoken audio. It supports local playback, generated audio files, Noiz AI TTS, and optional timeline rendering workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Assistant replies or supplied text may be sent to a cloud TTS service.

Mitigation: Avoid sensitive conversations unless the user accepts that data flow, and keep voice reply behavior explicitly opt-in.

Risk: The skill stores and uses a Noiz API key from the local environment or home directory.

Mitigation: Use least-privilege API keys, protect the key file, avoid exposing keys in command histories or logs, and rotate keys if exposed.

Risk: Runtime dependency installation and subprocess execution can modify the local environment.

Mitigation: Install dependencies in a controlled environment before use and review shell commands before execution.

Risk: Generated audio is saved and played locally, and previous generated audio may be deleted.

Mitigation: Confirm the output location and retention behavior before use, especially when preserving prior generated audio matters.

Risk: Reference audio may be fetched from URLs or uploaded for voice synthesis workflows.

Mitigation: Use only trusted reference audio sources and confirm that uploading reference audio is appropriate for the user and use case.

## Reference(s):

- [Voice Reply on ClawHub](https://clawhub.ai/richardx0319/skills/voice-reply-oc)
- [Noiz AI](https://noiz.ai)
- [Noiz API Keys](https://developers.noiz.ai/api-keys)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, API calls]

**Output Format:** [Audio files, SRT files, JSON reports, and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated audio can be saved as MP3, WAV, Opus, or Ogg/Opus depending on the command path.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
