## Description:

Converts Chinese and English text into MP3 speech with Edge-TTS or DashScope CosyVoice, with a slower default rate for English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjbook](https://clawhub.ai/user/bjbook)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can turn text or UTF-8 text files into spoken audio for language practice, notes, and other listening content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text sent for speech synthesis is transmitted to an external service.

Mitigation: Check text sensitivity before synthesis and send only material approved for the selected service.

Risk: DashScope credentials may be loaded from saved key files, and its endpoint is configurable.

Mitigation: Review automatic key-file lookup, use a dedicated key, and configure only an approved HTTPS endpoint.

Risk: The tool downloads audio from a URL returned by the service.

Mitigation: Restrict download destinations when running in environments that can access sensitive internal services.

## Reference(s):

- [zhz-tts on ClawHub](https://clawhub.ai/bjbook/skills/zhz-tts)
- [Project homepage](http://openclaw.bjbook.net/)

## Skill Output:

**Output Type(s):** [Audio files]

**Output Format:** [MP3 audio]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Speech audio with configurable engine, voice, rate, and volume.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
