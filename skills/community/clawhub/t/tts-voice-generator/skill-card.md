## Description:

Converts text into speech with selectable or uploaded custom voices through the Datamass TTS service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanfeng1234](https://clawhub.ai/user/seanfeng1234)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users use this skill to browse available voices, select or upload a reference voice, submit text-to-speech generation jobs, and check task status for generated audio URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send TTS text, voice samples, voice metadata, and API-key-authenticated requests to a remote Datamass endpoint.

Mitigation: Use it only if the Datamass service is trusted, avoid sensitive content, and verify the configured endpoint is the intended HTTPS Datamass host.

Risk: Audio uploads and paid generation may proceed with insufficient local validation or confirmation.

Mitigation: Validate audio file type and path, and require explicit confirmation before uploads or paid generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seanfeng1234/skills/tts-voice-generator)
- [Datamass service](https://www.datamass.cn)

## Skill Output:

**Output Type(s):** [text, API calls, configuration, guidance]

**Output Format:** [JSON-like dictionaries and human-readable status text with generated audio URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Datamass API key in ~/.openclaw/config.json; submits asynchronous TTS jobs and may return time-limited audio URLs.]

## Skill Version(s):

1.3.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
