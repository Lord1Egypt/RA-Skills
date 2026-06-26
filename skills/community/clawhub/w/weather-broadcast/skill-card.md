## Description: <br>
Fetch weather data and generate a spoken weather broadcast using SenseAudio TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scikkk](https://clawhub.ai/user/scikkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to fetch current weather, compose a short weather report, and generate spoken broadcast audio through SenseAudio TTS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather locations and broadcast text are sent to external weather and TTS services. <br>
Mitigation: Avoid sensitive locations or private operational context in generated broadcast text, and review provider terms before use. <br>
Risk: The SenseAudio API key can be exposed if pasted into prompts, logs, shared scripts, or committed files. <br>
Mitigation: Store SENSEAUDIO_API_KEY in a protected environment or secret manager and avoid printing it in generated commands. <br>
Risk: The examples write response.json and generated audio files to local storage. <br>
Mitigation: Review file contents and retention needs, and delete generated files when they contain sensitive or unwanted information. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/scikkk/weather-broadcast) <br>
- [SenseAudio Documentation](https://senseaudio.cn/docs) <br>
- [SenseAudio TTS API](https://senseaudio.cn/docs/text_to_speech_api) <br>
- [SenseAudio Voice List](https://senseaudio.cn/docs/voice_api) <br>
- [wttr.in Help](https://wttr.in/:help) <br>
- [Open-Meteo Docs](https://open-meteo.com/en/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples may create response.json and audio files locally when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
