## Description:

Generates two-host podcast audio from a topic or script using SenseAudio TTS, optional LLM script generation, voice selection, and speed or pitch controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cowboy231](https://clawhub.ai/user/cowboy231)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate MP3 podcast episodes from short topics or prepared scripts, either through a local web UI or chat-based agent flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated audio can be uploaded automatically to a hard-coded Feishu cloud folder using local OpenClaw credentials.

Mitigation: Require an explicit user-selected cloud folder, disable IM sending by default, and constrain Feishu upload permissions before deployment.

Risk: Tests and generation flows can call live services with production credentials.

Mitigation: Run tests with sandbox credentials or mocks, and avoid central OpenClaw credentials unless they are required for the release environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cowboy231/skills/senseaudio-podcast-generator)
- [SenseAudio homepage](https://senseaudio.cn)
- [Agent API guide](references/AGENT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance, JSON command results, API requests, and generated MP3 audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY and FFmpeg; Feishu delivery may upload generated audio to cloud storage.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
