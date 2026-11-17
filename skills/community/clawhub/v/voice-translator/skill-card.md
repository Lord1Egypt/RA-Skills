## Description:

Voice Translator helps agents turn spoken Chinese into spoken output in English, Japanese, or Korean, with scenario-aware translation, bidirectional conversation mode, and saved phrase favorites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to guide an agent through speech recognition, context-aware translation, text-to-speech playback, bidirectional conversation, and phrase favorites for travel and daily communication scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recorded speech and translated text may be sent to SenseAudio and any configured LLM provider.

Mitigation: Use the skill only for conversations where that cloud processing is acceptable, and avoid highly sensitive medical, financial, or private content unless provider handling has been reviewed.

Risk: Saved favorites and generated audio files can remain as local records.

Mitigation: Review, protect, and delete local favorites and temporary audio files according to the user's retention needs.

Risk: The skill requires a SenseAudio API key.

Mitigation: Provide the key through SENSEAUDIO_API_KEY and avoid placing credentials in prompts, source files, or shared logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scikkk/skills/voice-translator)
- [SenseAudio documentation](https://senseaudio.cn/docs)
- [SenseAudio ASR API](https://senseaudio.cn/docs/asr_api)
- [SenseAudio TTS API](https://senseaudio.cn/docs/text_to_speech_api)
- [SenseAudio language support](https://senseaudio.cn/docs/asr_api#language-support)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash, Python, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY and local curl and python3; may produce translated text, synthesized audio files, and saved favorites.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
