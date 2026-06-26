## Description: <br>
Voice Translator helps users speak Chinese and receive spoken translations in English, Japanese, Korean, and other supported languages, with scenario-aware translation, bidirectional conversation mode, and saved phrase favorites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travelers use this skill to turn spoken Chinese into natural target-language speech for restaurants, airports, hotels, taxis, shopping, medical visits, and other daily communication scenarios. Developers can adapt the included Python and curl examples to connect SenseAudio ASR/TTS and their chosen LLM translation provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recorded speech, transcripts, and translated text may be sent to SenseAudio and any LLM provider connected by the user. <br>
Mitigation: Use the skill only for conversations appropriate for those providers, and review provider privacy terms before using it for sensitive speech. <br>
Risk: The SENSEAUDIO_API_KEY is required for API calls. <br>
Mitigation: Protect the API key in environment or secret storage and avoid committing it to files or logs. <br>
Risk: Saved favorites can leave phrases on local or synced storage. <br>
Mitigation: Avoid saving favorites on shared or synced devices unless retaining those phrases is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/scikkk/voice-translator) <br>
- [SenseAudio Documentation](https://senseaudio.cn/docs) <br>
- [SenseAudio ASR API](https://senseaudio.cn/docs/asr_api) <br>
- [SenseAudio TTS API](https://senseaudio.cn/docs/text_to_speech_api) <br>
- [SenseAudio Language Support](https://senseaudio.cn/docs/asr_api#language-support) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY, curl, and python3; runtime behavior may call external ASR, LLM translation, and TTS services.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
