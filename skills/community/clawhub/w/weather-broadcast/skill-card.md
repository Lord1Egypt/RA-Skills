## Description:

Fetch weather data and generate a spoken weather broadcast using SenseAudio TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to fetch current weather, compose a short forecast script, and convert it into spoken audio with SenseAudio TTS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather locations and generated broadcast text may be sent to third-party services.

Mitigation: Avoid precise home or work addresses and omit sensitive personal details from broadcast text.

Risk: The SenseAudio API key is used when calling the SenseAudio TTS service.

Mitigation: Store the API key in the SENSEAUDIO_API_KEY environment variable and avoid committing it to skill files, logs, or generated examples.

Risk: Generated response and audio files may contain user-provided location or broadcast content.

Mitigation: Review generated files before sharing and handle them according to the user's data retention requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/scikkk/skills/weather-broadcast)
- [SenseAudio Documentation](https://senseaudio.cn/docs)
- [SenseAudio TTS API](https://senseaudio.cn/docs/text_to_speech_api)
- [SenseAudio Voice List](https://senseaudio.cn/docs/voice_api)
- [wttr.in Help](https://wttr.in/:help)
- [Open-Meteo Documentation](https://open-meteo.com/en/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with bash and Python examples that can produce weather text, JSON API responses, and audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SenseAudio API key for TTS calls; examples use curl, jq, wttr.in, Open-Meteo, and SenseAudio.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
